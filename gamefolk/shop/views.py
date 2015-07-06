"""Shop-related views."""

from functools import wraps
import http
from itertools import chain
import json

import flask
from flask import Blueprint, flash, redirect, request, render_template, url_for
from flask.ext.security.core import current_user
from flask.ext.security.decorators import login_required
import requests
import stripe
from werkzeug.datastructures import ImmutableOrderedMultiDict

from gamefolk import app, db
from gamefolk.shop.models import PaymentSource, Transaction
from gamefolk.users.models import User, create_secret_code

# pylint: disable=invalid-name

mod = Blueprint('shop', __name__, url_prefix='/shop')

IPN_VERIFY_PARAMS = (('cmd', '_notify-validate'),)

# Set up payment details
if app.debug:
    IPN_URL = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
    stripe.api_key = app.config['STRIPE_TEST_SECRET_KEY']
    STRIPE_PUBLISHABLE_KEY = app.config['STRIPE_TEST_PUBLISHABLE_KEY']
else:
    IPN_URL = 'https://www.paypal.com/cgi-bin/webscr'
    stripe.api_key = app.config['STRIPE_SECRET_KEY']
    STRIPE_PUBLISHABLE_KEY = app.config['STRIPE_PUBLISHABLE_KEY']


@mod.route('/')
def shop():
    """The main view of the shop. Contains information about the cartridge."""
    return render_template('shop/shop.html')


@mod.route('/purchase')
@login_required
def purchase():
    """The view that redirects the user to PayPal if they wish to buy a
    cartridge."""
    cartridge_cost = app.config['CARTRIDGE_COST']
    return render_template('shop/purchase.html',
                           cartridge_cost=cartridge_cost,
                           stripe_key=STRIPE_PUBLISHABLE_KEY)


@mod.route('/complete-payment')
@login_required
def complete_payment():
    """Route to visit after completed payment."""
    flash('Payment completed!', 'success')
    return render_template('shop/complete_payment.html')


@mod.route('/charge', methods=['POST'])
@login_required
def stripe_charge():
    """Handles transactions from Stripe"""
    cartridge_cost = app.config['CARTRIDGE_COST']

    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        card=request.form['stripeToken']
    )

    stripe.Charge.create(customer=customer.id,
                         amount=cartridge_cost,
                         currency='usd',
                         description='Cartridge Purchase',
                         metadata={'user_id': current_user.id})

    return redirect(url_for('shop.complete_payment'))


def ordered_storage(route):
    """Ensures that requests are processed in the correct order."""
    @wraps(route)
    def decorator(*args, **kwargs):
        """Stores request parameters in an ordered dictionary."""
        flask.request.parameter_storage_class = ImmutableOrderedMultiDict
        return route(*args, **kwargs)
    return decorator


def record_transaction(transaction_id, user_id, payment_source):
    """
    Store a successful transaction and generate a user's secret code.

    Parameters
    ----------
    transaction_id : str
        A unique identifier of the transaction.

    user_id : str
        The id of the user that made the transaction.

    payment_source : PaymentSource
        The payment provider that handled the transaction.
    """
    existing_transaction = Transaction.query.filter_by(
        transaction_id=transaction_id,
        payment_source=payment_source.value).first()
    if existing_transaction:
        app.logger.warning('Duplicate transaction %s encountered',
                           transaction_id)
        return json.dumps({'status': 'failure'})
    transaction = Transaction(transaction_id=transaction_id,
                              user_id=user_id,
                              payment_source=payment_source.value)
    db.session.add(transaction)
    db.session.commit()
    purchasing_user = User.query.filter_by(id=int(user_id)).one()
    purchasing_user.secret_code = create_secret_code()
    db.session.commit()
    app.logger.info('Complete %s transaction %s recorded',
                    payment_source.value,
                    transaction_id)


def validate_ipn(response, ipn_message):
    """Validates an ipn message according to PayPal's recommendations."""
    intended_recipient = app.config['PAYPAL_MERCHANT_EMAIL']
    return (response.text == 'VERIFIED' and
            ipn_message['receiver_email'] == intended_recipient)


@mod.route('/stripe-webhooks', methods=['POST'])
def stripe_webhook():
    """Webhook for completed Stripe charges."""
    event = request.json
    app.logger.debug('Received stripe webhook: %s',
                     json.dumps(event, indent=4, sort_keys=True))

    if event['type'] == 'charge.succeeded':
        transaction_id = event['data']['object']['id']
        user_id = event['data']['object']['metadata']['user_id']
        record_transaction(transaction_id, user_id, PaymentSource.stripe)

    return ('', http.client.NO_CONTENT)


@mod.route('/ipn', methods=['POST'])
@ordered_storage
def instant_payment_notification():
    """Callback for PayPal's instant payment notifications."""
    ipn_message = request.form
    verify_params = chain(ipn_message.items(), IPN_VERIFY_PARAMS)
    response = requests.post(IPN_URL, params=dict(verify_params))
    if not validate_ipn(response, ipn_message):
        app.logger.warning('PayPal IPN {arg} did not validate',
                           arg=ipn_message)
        return json.dumps({'status': 'failure'})

    if ipn_message['payment_status'] == 'Completed':
        transaction_id = ipn_message['txn_id']
        user_id = ipn_message['custom']
        record_transaction(transaction_id, user_id, PaymentSource.paypal)

    return json.dumps({'status': 'complete'})


@mod.route('/verify-code')
def verify_code():
    """Verifies that a user's email is associated with a given secret code."""
    email = request.args.get('email')
    code = request.args.get('code')
    user = User.query.filter_by(email=email).first()
    if user and user.secret_code == code:
        return 'true'
    else:
        return 'false', http.client.UNAUTHORIZED

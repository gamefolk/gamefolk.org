"""Shop-related views."""

from functools import wraps
import http
from itertools import chain
import json
import logging

import flask
from flask import Blueprint, flash, request, render_template
from flask.ext.login import login_required
import requests
from werkzeug.datastructures import ImmutableOrderedMultiDict

from gamefolk import app, db
from gamefolk.shop.models import Transaction
from gamefolk.users.models import User, create_secret_code

mod = Blueprint('shop', __name__, url_prefix='/shop')

IPN_VERIFY_PARAMS = (('cmd', '_notify-validate'),)
if app.debug:
    IPN_URL = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
else:
    IPN_URL = 'https://www.paypal.com/cgi-bin/webscr'


@mod.route('/')
@login_required
def shop():
    """The main view for the shop."""
    return render_template('shop/shop.html')


@mod.route('/complete-payment')
@login_required
def complete_payment():
    """Route to visit after completed payment."""
    flash('Payment completed!', 'success')
    return render_template('shop/complete_payment.html')


def ordered_storage(route):
    """Ensures that requests are processed in the correct order."""
    @wraps(route)
    def decorator(*args, **kwargs):
        """Stores request parameters in an ordered dictionary."""
        flask.request.parameter_storage_class = ImmutableOrderedMultiDict
        return route(*args, **kwargs)
    return decorator


def record_transaction(transaction_id, user_id):
    """Store a successful PayPal transaction and generate a user's secret
    code."""
    existing_transaction = Transaction.query.filter_by(
        transaction_id=transaction_id).first()
    if existing_transaction:
        logging.warning('Duplicate transaction {id} encountered',
                        id=transaction_id)
        return json.dumps({'status': 'failure'})
    transaction = Transaction(transaction_id=transaction_id, user_id=user_id)
    db.session.add(transaction)
    db.session.commit()
    purchasing_user = User.query.filter_by(id=int(user_id)).first()
    purchasing_user.secret_code = create_secret_code()
    db.session.commit()
    logging.info('Complete transaction {id} recorded', id=transaction_id)


def validate_ipn(response, ipn_message):
    """Validates an ipn message according to PayPal's recommendations."""
    intended_recipient = app.config['PAYPAL_MERCHANT_EMAIL']
    return (response.text == 'VERIFIED' and
            ipn_message['receiver_email'] == intended_recipient)


@mod.route('/ipn', methods=['POST'])
@ordered_storage
def instant_payment_notification():
    """Callback for PayPal's instant payment notifications."""
    ipn_message = request.form
    verify_params = chain(ipn_message.items(), IPN_VERIFY_PARAMS)
    response = requests.post(IPN_URL, params=dict(verify_params))
    if not validate_ipn(response, ipn_message):
        logging.warning('PayPal IPN {arg} did not validate', arg=ipn_message)
        return json.dumps({'status': 'failure'})

    if ipn_message['payment_status'] == 'Completed':
        transaction_id = ipn_message['txn_id']
        user_id = ipn_message['custom']
        record_transaction(transaction_id, user_id)

    return json.dumps({'status': 'complete'})


@mod.route('/verify-code')
def verify_code():
    """Verifies that a user's email is associated with a given secret code."""
    email = request.args.get('email')
    code = request.args.get('code')
    user = User.query.filter_by(email=email).first()
    if user and user.secret_code == code:
        return json.dumps({'success': True})
    else:
        return json.dumps({
            'error': 'either a user with that email does not exist or the '
                     'code is incorrect.'
        }), http.client.UNAUTHORIZED

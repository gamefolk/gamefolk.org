"""Shop-related views."""

from functools import wraps
from itertools import chain
import json

import flask
from flask import Blueprint, request, render_template
from flask.ext.login import login_required
import requests
from werkzeug.datastructures import ImmutableOrderedMultiDict

from gamefolk_shop import app

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

def ordered_storage(route):
    """Ensures that requests are processed in the correct order."""
    @wraps(route)
    def decorator(*args, **kwargs):
        """Stores request parameters in an ordered dictionary."""
        flask.request.parameter_storage_class = ImmutableOrderedMultiDict
        return route(*args, **kwargs)
    return decorator

@mod.route('/ipn', methods=['POST'])
@ordered_storage
def instant_payment_notification():
    """Callback for PayPal's instant payment notifications."""
    ipn_message = request.form
    verify_params = chain(ipn_message.items(), IPN_VERIFY_PARAMS)
    response = requests.post(IPN_URL, params=dict(verify_params))
    if (response.text != 'VERIFIED' or
            ipn_message['receiver_email'] != app.config['PAYPAL_MERCHANT_EMAIL']):
        print('PayPal IPN {arg} did not validate' % ipn_message)
        return json.dumps({'status': 'failure'}), 400

    if ipn_message['payment_status'] == 'Completed':
        print('User with id ' + ipn_message['custom'] + ' paid!')

    return json.dumps({'status': 'complete'})

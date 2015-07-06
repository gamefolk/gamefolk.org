"""Views for the shop."""

from enum import Enum, unique

from gamefolk import db

# pylint: disable=invalid-name, too-few-public-methods


@unique
class PaymentSource(Enum):
    """Payment handlers that the application supports."""
    paypal = 'PayPal'
    stripe = 'Stripe'


class Transaction(db.Model):
    """A completed transaction for an item bought in the shop."""

    id = db.Column(db.Integer, primary_key=True)

    # The transaction ID provided by the payment handler
    transaction_id = db.Column(db.String(20))

    # The user who completed the transaction
    user_id = db.Column(db.Integer)

    # pylint: disable=no-member
    payment_source = db.Column(db.Enum(*PaymentSource.__members__.keys()))
    # pylint: enable=no-member

    def __init__(self, transaction_id, user_id, payment_source):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.payment_source = payment_source

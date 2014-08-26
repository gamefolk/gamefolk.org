from gamefolk import db


class Transaction(db.Model):
    """A completed PayPal transaction."""
    id = db.Column(db.Integer, primary_key=True)        # pylint: disable=C0103

    # The transaction ID provided by PayPal
    transaction_id = db.Column(db.String(20), unique=True)

    # The user who completed the transaction
    user_id = db.Column(db.Integer)

    def __init__(self, transaction_id, user_id):
        self.transaction_id = transaction_id
        self.user_id = user_id

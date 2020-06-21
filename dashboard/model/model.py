import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Trip(db.Model):
    """Define a Trip."""

    __tablename__ = 'trip_train_after_mm_2'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __unicode__(self):
        """Give a readable representation of an instance."""
        return '{}'.format(self.name)

    def __repr__(self):
        """Give a unambiguous representation of an instance."""
        return '<{}#{}>'.format(self.__class__.__name__, self.id)
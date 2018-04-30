
from sqlalchemy import SQLAlchemy

engine = create_engine('sqlite:////tmp/base.db', echo=True)

connection=engine.connect()

class Base(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<User %r>' % self.username

connection.close()

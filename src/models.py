from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    datasheet = db.Column(db.String(255))
    image = db.Column(db.String(255))
    io_number = db.Column(db.Integer)
    io_state = db.Column(db.Boolean, default=False)
    barcode = db.Column(db.String(255))
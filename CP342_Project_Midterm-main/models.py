from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()

class info(db.Model):
    dev_id = db.Column(db.Integer(), primary_key=True)
    dev_name  = db.Column(db.String())
    dev_pic = db.Column(db.String())
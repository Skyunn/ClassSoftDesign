from static import db #import the db which can be found in __init__
from datetime import datetime

# Associative Table for Item <-> User Relationship (m2m)
item_user_association = db.Table(
    'purchase',
    db.Column('id', db.Integer, primary_key = True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), nullable = True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable = True),
    db.Column('dataPurchased', db.Date, default = datetime.now)
)

class Item(db.Model): 
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    price = db.Column(db.Integer, nullable = False, default = 50)
    quantity = db.Column(db.Integer, nullable = False, default = 50)
    # datePurchased = db.Column(db.Date, default = datetime.utcnow)
    type = db.Column(db.String(50), nullable = True)
    description = db.Column(db.String(), nullable = True)

    def __repr__(self):
        return f'{self.name}'
    
    # Define the m2m relationship with user entity
    owners = db.relationship('User', secondary=item_user_association,
                             backref=db.backref('items_owned', lazy='dynamic'),
                             overlaps='items_owned, owners')


    __mapper_args__ = {
        'polymorphic_identity': 'item',
        'polymorphic_on': type # Designate what fields to differentiate attributes
    }

class Electronics(Item): 
    __tablename__ = 'electronics'
    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key = True)
    # Unique Fields for Electronics Subclass
    manufacturer = db.Column(db.String(), nullable = False)

    __mapper_args__ = {
        'polymorphic_identity': 'electronics',
    }

class Clothing(Item):
    __tablename__ = 'clothing'
    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key = True)
    # Unique Fields for Electronics Subclass
    brand = db.Column(db.String(), nullable = False)

    __mapper_args__ = {
        'polymorphic_identity': 'clothing',
    }

class Food(Item):
    __tablename__ = 'food'
    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key = True)
    # Unique Fields for Electronics Subclass
    isHalalCertified = db.Column(db.String(), nullable = False)

    __mapper_args__ = {
        'polymorphic_identity': 'food',
    }

class User(db.Model): 
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    balance = db.Column(db.Integer, nullable = False, default = 50)
    birthDate = db.Column(db.Date, default = datetime.utcnow)
    description = db.Column(db.String(), nullable = True)
    # Define te m2 relationship with item entity
    owned_items = db.relationship('Item', secondary = item_user_association,
                                  backref=db.backref('purchasors', lazy='dynamic'))
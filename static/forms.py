from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, BooleanField
from wtforms.fields import DateField
from wtforms.validators import Length, DataRequired, ValidationError
from datetime import datetime

class ItemForm(FlaskForm): 
    name = StringField(label='Name: ', validators=[Length(min=5, max=200), DataRequired()])
    price = IntegerField(label='Price: ', validators=[DataRequired()])
    description = StringField(label='Description')
    type = StringField('Type')
    # type = SelectField(choices=[('Electronic'), ('Medicine'), ('Food'), ('Misc')])
    # datePurchased = DateField(label='Date: ', validators=[DataRequired()], default=datetime.today().date)
    submit = SubmitField(label='Submit')

class ElectronicsForm(ItemForm):
    manufacturer = StringField('Manufacturer', validators=[DataRequired()])

class ClothingForm(ItemForm):
    brand = StringField('Brand', validators=[DataRequired()])

class FoodForm(ItemForm):
    isHalalCertified = BooleanField('Halal Certified')

class PurchaseForm(FlaskForm):
    itemToBuy = StringField('Item', validators=[DataRequired()])
    buyer = StringField('Buyer', validators=[DataRequired()])
    # datePurchased = SubmitField('Date Purchased', validators=[DataRequired()], default=datetime.today().date)
    datePurchased = DateField(label='Date: ', validators=[DataRequired()], default=datetime.today().date)
    submit = SubmitField(label='Submit')
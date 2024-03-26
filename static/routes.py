from static import app, db
from flask import render_template,request,redirect,url_for,get_flashed_messages,flash

#import the classes from entities.py
from static.entities import *
import locale
from static.forms import *


@app.route('/')
@app.route('/main')
def index():
    #return "Hello, World!"
    return redirect(url_for('search'))

@app.route('/search', methods = ['GET','POST'])
def search():
    query = request.args.get('query','')
    category = request.args.get('category')
    if category == "Electronics":
        results = Electronics.query.filter(Electronics.name.ilike(f"%{query}%") | Electronics.id.ilike(f"%{query}%")).all()
    elif category == "Clothing":
        results = Clothing.query.filter(Clothing.name.ilike(f"%{query}%") | Clothing.id.ilike(f"%{query}%")).all()
    elif category =="Food":
        results = Food.query.filter(Food.name.ilike(f"%{query}%") | Food.id.ilike(f"%{query}%")).all()
    else:
        results = Item.query.filter(Item.name.ilike(f"%{query}%") | Item.id.ilike(f"%{query}%")).all() 
    itemFormatted = FormatItem(results)
    form = ElectronicsForm()
    return render_template('index.html',items=itemFormatted,query=query,form=form,category=category)

@app.route('/UpdateItem/<int:item_id>',methods=['GET','POST'])
def updateItem(item_id):
    ItemToUpdate = Item.query.filter_by(id=item_id).first()
    form = ElectronicsForm(obj=ItemToUpdate) #pre-populate the form data using attributes of the ItemToUpdate
    if form.validate_on_submit():
        form.populate_obj(ItemToUpdate)
        db.session.commit()
        flash('Success! The update has been committed to the database', category='success')
        return redirect(url_for('index'))
    CheckFormError(form)
    return render_template('UpdateItem.html',form=form)
    
@app.route('/DeleteItem/<int:item_id>',methods=['GET','POST']) # Specifiy of the data type of the argument 
def deleteItem(item_id):
    ItemToDelete = Item.query.filter_by(id=item_id).first()
    if ItemToDelete:
        db.session.delete(ItemToDelete)
        db.session.commit()
        flash('Item has been deleted', category='success')
    return redirect(url_for('index'))

    
@app.route('/register_electronics',methods = ['GET', 'POST'])
def registerElectronics():
    form = ElectronicsForm()
    if form.validate_on_submit():
        elec_to_create = Electronics(name = form.name.data,
                            price=form.price.data
                            ,description=form.description.data,
                            manufacturer=form.manufacturer.data)
        similarElec = Electronics.query.filter(Electronics.name.ilike(f'%{elec_to_create}%')).all()
        if similarElec:
            flash(f'Item {elec_to_create.name} is already in the database', category='warning')
        else:
            db.session.add(elec_to_create)
            db.session.commit()
            flash('Success! Item has been created',category='success')

            #display recently addedd item on first tuple
            query = request.args.get('query','')
            results = Item.query.filter(Item.name.ilike(f"%{query}%")).all()
            results = FormatItem(results)
            results = [results[-1]] + results[:-1] # last index of the list becomes the first
            return render_template('index.html',items=results,query=query,form=form) #space sensitive
        
        #return redirect(url_for('index',items=results,query=query,form=form))

    CheckFormError(form)
    return redirect(url_for('search'))

def CheckFormError(form):
    if form.errors != {}:
        for errorMessage in form.errors.values():
            flash(f'Error: {errorMessage}' ,category='alert')

@app.route('/purchase/<int:item_id>', methods = ['GET', 'POST'])
def registerPurchase(item_id):
    ItemToBuy = Item.query.filter_by(id=item_id).first()
    form = PurchaseForm()
    form.itemToBuy.data = ItemToBuy.id # Pre-populate
    if form.validate_on_submit:
        purchase_to_create = item_user_association.insert().values(
                            item_id=form.itemToBuy.data,
                            buyer=form.buyer.data,
                            datePurchased=form.datePurchased.data)
        db.session.add(purchase_to_create)
        db.session.commit()
        flash('Success! Purchase had been made',category='success')

        #display recently addedd item on first tuple
        query = request.args.get('query','')
        results = Item.query.filter(Item.name.ilike(f"%{query}%")).all()
        results = FormatItem(results)
        results = [results[-1]] + results[:-1] # last index of the list becomes the first
        return render_template('index.html',items=results,query=query,form=form) #space sensitive

    CheckFormError(form)
    return render_template('Purchase.html', form=form)

def FormatItem(items):
    locale.setlocale(locale.LC_ALL,'')
    month_names = ['January','Febuary','March','April','May','June','July','August','September','October','November'
                   ,'December']
    # modify the formatting fof DatePurchased and Price
    for item in items:
        item.price = locale.format_string("%.2f",item.price, grouping=True)
        #month_name = month_names[item.datePurchased.month - 1]
       # item.datePurchased = f"{month_name} {item.datePurchased.day},{item.datePurchased.year}"
    return items
    

import json

from flask import Blueprint, render_template, request, jsonify
from sqlalchemy import extract, and_, desc
from datetime import datetime

from ... import app, db
from ...models import DEntry, CEntry


home_bp = Blueprint('home', __name__, template_folder='templates')

@home_bp.route('/', methods=['GET', 'POST'])
def home():
    '''
    Get the data from db for Highest Sales by Customer and Monthly Sales for JS Charts
    '''
    '''NEED FIX'''
    # Highest Sales by Customer
    names = [items.name for items in CEntry.query.join(DEntry).order_by(desc(DEntry.price))]
    prices = [int(items.price) for items in DEntry.query.all()]
    prices = sorted(prices, reverse=True)

    # Create string of list of names of highest puchases to send to graph in home page through home.js
    names_str = ""
    price_str = ""
    for name,price in zip(names,prices):
        names_str += name[:15]+','
        price_str += str(price)+','

    # Monthly Sales 
    Query_time = db.session.query(DEntry.time)
    Query_price = db.session.query(DEntry.price)
    current_year, current_month = datetime.now().year, datetime.now().month
    months_for_monthly_sale = []
    list_datetime = []
    list_price = []

    #getting list of datetimes and respective prices of purchase on monthly basis of past 12 months
    for i in range(current_month, current_month-12, -1):
        if i == 0:
            current_year -= 1
            current_month = 12
        list_datetime += [Query_time.filter(
          and_(  
            extract('year', DEntry.time) == current_year,
            extract('month', DEntry.time) == current_month
              )
            ).all()]
        list_price += [Query_price.filter(
          and_(  
            extract('year', DEntry.time) == current_year,
            extract('month', DEntry.time) == current_month
              )
            ).all()]
        months_for_monthly_sale += [current_month]
        current_month -= 1
    
    # Sum of prices for each month
    monthly_sale = []
    monthly_total = 0
    for price in list_price:
        for items in price:
            monthly_total += int(items[0])
        monthly_sale += [monthly_total]
        monthly_total = 0     

    # POST request from client to fetch monthly sales data which is passed here
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8'))
        if data['key'] == "montlySalesGraph":
            return jsonify({'monthly_sale':monthly_sale, 'months':months_for_monthly_sale})

    return render_template('home/home.html', data=names_str, price=price_str)

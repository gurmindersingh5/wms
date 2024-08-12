import json

from datetime import datetime
from flask import Blueprint, render_template, request, jsonify
from sqlalchemy import extract, and_, desc, func

from ... import app, db
from ...models import DEntry, CEntry
from ...thousand_seperator import thousand_seperator_func

home_bp = Blueprint('home', __name__, template_folder='templates')

@home_bp.route('/', methods=['GET', 'POST'])
def home():
    '''
    Get the data from db for Highest Sales by Customer and Monthly Sales for JS Charts
    '''


    # Highest Sales by Customer
    '''
    SELECT C.name, SUM(D.price) as total_purchases_amount
    FROM DEntry D
    JOIN CEntry C
    ON D.cust_id = C.cust_id
    GROUP BY C.cust_id
    ORDER BY total_purchases_amount DESC
    ;
    '''
    results = db.session.query(
        CEntry.name, 
        db.func.sum(DEntry.price).label('total_purchases_amount')
    ).join(
        DEntry, CEntry.cust_id == DEntry.cust_id
    ).group_by(
        CEntry.cust_id
    ).order_by(
        db.desc('total_purchases_amount')
    ).all()
    names = [item.name for item in results] 
    prices = [float(item.total_purchases_amount) for item in results] 
 
     # Create string of list of names of highest puchases to send to graph in home page through home.js
    names_str = ""
    price_str = ""
    for name, price in zip(names, prices): 
        names_str += name[:15]+','
        price_str += str(price)+' '

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

    return render_template('home/home.html', data=names_str, price=prices)



@home_bp.route('/api/fetch_data', methods=['GET', 'POST'])
def fetch_data():
    '''
    SELECT strftime('%Y-%m', time) as date_, SUM(price) as sales
    FROM d_entry
    GROUP BY strftime('%Y-%m', time);
    '''

    results = db.session.query(
        func.strftime('%Y-%m', DEntry.time).label('year_month'),
        func.sum(DEntry.price).label('monthly_sales')
    ).group_by(
	func.strftime('%Y-%m', DEntry.time)
    ).all()
    year_month = []
    monthly_sales = []
    for r in results:
        y_m, m_s = r
        year_month.append(y_m)
        monthly_sales.append(int(m_s))

    return jsonify({
        'year_month': year_month,
        'monthly_sales': monthly_sales
        })

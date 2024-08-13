from flask import Blueprint, jsonify, abort
from sqlalchemy import func

from ...models import DEntry, CEntry, PEntry
from ...extensions import db


analytics_api_bs = Blueprint('analytics_api_bs', __name__)

@analytics_api_bs.route('/api/fetch_data/<slug>', methods=['GET'])
def fetch_data(slug: str):
    '''
    API to return various data realted queries for plotly dash.
    All queries for Plotly must be performed here.
    Returnable queries are Monthly sales, Stock level, 
    '''

    # Monthly sales 
    def get_monthly_sales():
        '''
        Query to fetch monthly sales data.
        SELECT strftime('%Y-%m', time) as date_, SUM(price) as sales
        FROM d_entry
        GROUP BY strftime('%Y-%m', time);
        '''
        try:
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
        except Exception as e:
            # Handle any exceptions that occur during the query
            print(f"Error fetching monthly sales data: {e}")
            abort(500, description="Internal server error")

            
    # stock levels
    def get_stock_levels():
        '''
        SELECT part_id AS id, name, (container_qty*container_capacity+pieces_qty) AS qty_remaining
        FROM p_entry
        ORDER BY qty_remaining ASC
        LIMIT 10;
        ;
        '''
        try:
            stock_levels_data = db.session.query(
                PEntry.name, PEntry.container_qty*PEntry.container_capacity+PEntry.pieces_qty
            ).order_by(
                (PEntry.container_qty*PEntry.container_capacity+PEntry.pieces_qty).asc()
            ).limit(10).all() 

            stock_levels = [
            {
                'name': name,
                'qty_remaining': qty_remaining
            } for name, qty_remaining in stock_levels_data
            ]
            print(stock_levels, '+++++')
            return jsonify({
                'stock_levels': stock_levels
            })
        except Exception as e:
            print(f"Error fetching stock levels data: {e}")
            abort(500, description="Internal server error")
    
    if slug == 'monthly_sales':
        return get_monthly_sales()
    elif slug == 'stock_levels':
        return get_stock_levels()
    else:
        # If the slug does not match any known endpoint, return a 404 error
        abort(404, description="Resource not found")


import dash
import plotly.graph_objs as go

from dash import dcc, html
from dash.dependencies import Input, Output
from flask import Blueprint, redirect, url_for

from ..blueprints.analytics_api.analytics_api import fetch_data
from .fetchdata import fetch_data

def init_dash_app(flask_app): # server is flask app
    dash_bp = Blueprint('dashapp', __name__, url_prefix='/dash')

    # need this route to be able to use url_for('dashapp.index') in home.html
    @dash_bp.route('/')
    def index():
        return redirect(url_for('dashapp.dash_index'))

    app = dash.Dash(
        __name__,
        server=flask_app,
        url_base_pathname='/dash/',
        suppress_callback_exceptions=True
    )

    # Restructure the data to separate by year
    def restructure_data(data):
        monthly_sales = data['monthly_sales']
        year_month = data['year_month']

        # Create dictionaries to separate sales data by year
        sales_by_year = {}
        for ym, sale in zip(year_month, monthly_sales):
            year = ym.split('-')[0]
            if year not in sales_by_year:
                sales_by_year[year] = []
            sales_by_year[year].append(sale)

        return sales_by_year

    app.layout = html.Div([
        html.H4('Monthly Sales Data Over 4 Years'),
        dcc.Checklist(
            id='year-selector',
            options=[
                {'label': '2021', 'value': '2021'},
                {'label': '2022', 'value': '2022'},
                {'label': '2023', 'value': '2023'},
                {'label': '2024', 'value': '2024'},
            ],
            value=['2024', '2023', '2022', '2021'],  # Default selection
            labelStyle={'display': 'inline-block', 'margin-right': '10px'},
            inputStyle={'margin-right': '5px'}
        ),

        dcc.Graph(id='line-plot'), # for monthly sales

        html.H4('Low Inventory Stocks Levels'),
        dcc.Graph(id='bar-plot'), # for low inventory levels
    ], style={'backgroundColor': 'transparent', 'padding': '0px'})


    # SALES CHART
    @app.callback(
        Output('line-plot', 'figure'),
        [Input('year-selector', 'value')]
    )
    def update_sales_chart(selected_years):
        data = fetch_data('monthly_sales')

        sales_by_year = restructure_data(data)  # Get the restructured data

        fig = go.Figure()
        colors = {'2021': 'rgb(255, 99, 132)',
                '2022': 'rgb(54, 162, 235)',
                '2023': 'rgb(75, 192, 192)',
                '2024': 'blue'}
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        for year in selected_years:
            fig.add_trace(go.Scatter(
                x=months,  # Use the full months list
                y=sales_by_year[year],
                mode='lines+markers',
                name=f'Sales {year}',
                line=dict(color=colors[year], width=3, shape='spline', smoothing=0.5),
                marker=dict(size=5)
            ))

        # Styling the chart
        fig.update_layout(
            yaxis_title='Sales',
            plot_bgcolor='rgba(245, 245, 245, 1)',
            paper_bgcolor='rgba(255, 255, 255, 1)',
            font=dict(color='black'),
            xaxis=dict(showgrid=False, gridcolor='lightgray'),
            yaxis=dict(showgrid=True, gridcolor='white'),
            legend=dict(
                x=0.1, y=1.1,
                bgcolor='rgba(255, 255, 255, 0.5)',
                bordercolor='rgba(255, 255, 255, 0.8)'
            ),
            margin=dict(l=20, r=20, t=15, b=40)
        )
        return fig 


    # STOCK LEVEL CHART
    @app.callback(
        Output('bar-plot', 'figure'),
        [Input('year-selector', 'value')] # input not used here
    )
    def update_inventory_chart(selected_years):
        data = fetch_data('stock_levels')
        partname = [item['name'] for item in data['stock_levels']]
        stocklevel = [item['qty_remaining'] for item in data['stock_levels']][::-1]

        fig = go.Figure(go.Bar(
            x=stocklevel,
            y=partname,
            orientation='h',  # Horizontal bar chart
            marker=dict(
                color=stocklevel,
                colorscale='RdYlGn',  # Red to Green color scale
                cmin=min(stocklevel),  # Set the color scale minimum to the minimum quantity
                cmax=max(stocklevel),  # Set the color scale maximum to the maximum quantity
                colorbar=dict(
                    title='Stock Level',
                    tickvals=[min(stocklevel), max(stocklevel)],
                    ticktext=['Low', 'Safe'],
                ),
            )
        ))

        fig.update_layout(
            xaxis_title='Quantity Remaining',
            yaxis_title='Part Name',
            plot_bgcolor='rgba(245, 245, 245, 1)',
            paper_bgcolor='rgba(255, 255, 255, 1)',
            font=dict(color='black'),
            xaxis=dict(showgrid=True, gridcolor='white'), 
            yaxis=dict(showgrid=False),
            margin=dict(l=20, r=20, t=15, b=40)
        )
        return fig
    
    flask_app.register_blueprint(dash_bp)

    return app
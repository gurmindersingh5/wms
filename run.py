from app import app 

from app.blueprints.home.home import home_bp
from app.blueprints.inventory.inventory import inventory_bp
from app.blueprints.customer.customer import customer_bp
from app.blueprints.addproduct.addproduct import addproduct_bp
from app.blueprints.editproduct.editproduct import editproduct_bp
from app.blueprints.register.register import register_bp
from app.blueprints.sales.sales import sales_bp
from app.blueprints.addcustomer.addcustomer import addcustomer_bg
from app.blueprints.profile.profile import profile_bp
from app.blueprints.analytics_api.analytics_api import analytics_api_bs

from app.blueprints.login.login import login_bp
from app.blueprints.google.google import google_bp


app.register_blueprint(home_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(addproduct_bp)
app.register_blueprint(editproduct_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(addcustomer_bg)
app.register_blueprint(profile_bp)
app.register_blueprint(analytics_api_bs)

app.register_blueprint(google_bp, url_prefix="/login")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)


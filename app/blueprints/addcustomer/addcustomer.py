from flask import Blueprint, request, redirect, render_template, url_for
from ...form import Customer_Entry
from ...models import CEntry
from datetime import datetime
from ... import db

success_note = ""
addcustomer_bg = Blueprint('addcustomer', __name__, template_folder='templates')
@addcustomer_bg.route('/cform', methods=['GET', 'POST'])
def c_form():
    global success_note
    form_data = Customer_Entry()
    if request.method == "POST":
        if form_data.validate_on_submit():
            print(form_data.validate_on_submit())
            data = CEntry(name=form_data.name.data,
                          address=form_data.address.data,
                          contact=form_data.contact.data
                          )
            existing_customer = CEntry.query.filter_by(name=form_data.name.data).first()
            if existing_customer:
                return redirect(url_for('addcustomer.c_form')), 12
            else:
                db.session.add(data)
                db.session.commit()
                success_note = [data.name, data.address, data.contact, datetime.now().strftime('%d-%m-%Y ~ %H:%M')] 

            return redirect(url_for('addcustomer.c_form'))
    if form_data.errors != {}:
        for err_msg in form_data.errors.values():
            print(f" There was an error {err_msg}")
    return render_template('addcustomer/cform.html', form=form_data, success_note=success_note)



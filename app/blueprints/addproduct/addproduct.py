from datetime import datetime
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import  login_required

from ...models import PEntry
from ...form import Part
from ... import db

addproduct_bp = Blueprint('addproduct', __name__, template_folder='templates')


NOTE = ""
@addproduct_bp.route('/pform', methods=['GET', 'POST'])
@login_required
def p_form():
    global NOTE
    form = Part()
    if request.method == 'POST' and form.validate_on_submit():
        name=form.name.data.strip()
        price=form.price.data
        container_qty=form.container_qty.data
        pieces_qty=form.pieces_qty.data
        container_capacity=form.container_capacity.data

        data = PEntry(name=name,
                      price=price,
                      container_qty=container_qty,
                      pieces_qty=pieces_qty,
                      container_capacity=container_capacity,
                      )
        existing_product = PEntry.query.filter_by(name=name).first()
        if existing_product:
            flash('Product already exists with this name, please edit the existing product instead of creating new one.')
            return redirect(url_for('addproduct.p_form')), 400
        else:
            db.session.add(data)
            db.session.commit()
            NOTE = [data.name, data.price, datetime.now().strftime('%d-%m-%Y ~ %H:%M')]
            return redirect(url_for('addproduct.p_form'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            print(f" There was an error {err_msg}")
    return render_template('addproduct/pform.html', form=form, note=NOTE)


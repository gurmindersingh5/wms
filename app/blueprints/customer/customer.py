from flask import Blueprint, request, redirect, url_for, render_template, jsonify
from sqlalchemy import func
from collections import defaultdict

from ... import db
from ...form import search_form
from ...models import DEntry, CEntry, PEntry
from ...thousand_seperator import thousand_seperator_func

customer_bp = Blueprint('customer', __name__, template_folder='templates')


C_ID_FOR_customerdata = None
@customer_bp.route('/customerlist', methods=["GET", "POST"])
def customerlist():  
    query = db.session.query(CEntry)
    results = query.order_by(func.lower(CEntry.name)).all()    
    form_data = search_form()
    NOTE = ""
 
    if request.method == "POST":
        try:
            if request.json['custId']:
                global C_ID_FOR_customerdata
                C_ID_FOR_customerdata = request.json['custId']
                return redirect(url_for('customerdata_'))
        except Exception as e:
            print(str(e))

        results = []
        if form_data.data['S_name']:
            results += query.filter(CEntry.name.like(f"%{form_data.data['S_name']}%"))
        if form_data.data['S_address']:
            results += query.filter(CEntry.address.like(f"%{form_data.data['S_address']}%"))
        results = set(results)
    if not results:
        NOTE = "Not found in database"
    else:
        NOTE = f"{len(results)} entry/ies"
    return render_template('customer/customerlist.html', form=form_data, results=results, note=NOTE)


@customer_bp.route('/customerdata', methods=['GET', 'POST'])
def customerdata_():
    partlist = {}
    total = 0
    invoice_totals = {}
    if C_ID_FOR_customerdata:
        cust_id = C_ID_FOR_customerdata
        cust_data = db.session.query(CEntry).filter_by(cust_id=cust_id).first()
        purchased_data = db.session.query(DEntry).filter_by(cust_id=cust_id).order_by(DEntry.invoice_no.desc()).all()
        
        invoice_items = defaultdict(list)
        for entry in purchased_data:
            invoice_items[entry.invoice_no].append(entry)
        invoice_items = dict(invoice_items)

        total = 0
        for invoice_number, items in invoice_items.items():
            total2 = sum(item.price for item in items)
            invoice_totals[invoice_number] = thousand_seperator_func(total2)
            total += total2
        total = thousand_seperator_func(total)

        for item in purchased_data:
            partlist[item.part_id] = db.session.query(PEntry).filter_by(part_id=item.part_id).first().name

        return render_template('customer/customerdata.html', cust_data=cust_data, purchased_data=invoice_items, partlist=partlist, total=total, invoice_totals=invoice_totals)
    else:
        return jsonify({'error': 'Pls go back to Customer Inquiry and try again'})



@customer_bp.route('/delete_invoice', methods=['GET', 'POST'])
def delete_invoice():
    if request.json['invoiceNo']:    
        entries_to_delete = DEntry.query.filter_by(invoice_no=request.json['invoiceNo']).all()
        for entry in entries_to_delete:
            db.session.delete(entry)
        db.session.commit()
        return jsonify({'success': 'Deleted'}), 200
    

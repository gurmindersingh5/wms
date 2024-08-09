from flask import Blueprint, request, jsonify, render_template
from sqlalchemy import func

from ... import app, db
from ...models import CEntry, PEntry, DEntry, Invoice
from ...form import DataEntry

sales_bp = Blueprint('sales', __name__, template_folder='templates')

LASTENTRY = []
e_form_note = ""
PartID_for_e_form = None
next_invoice_number = None
@sales_bp.route('/eform', methods=['GET', 'POST'])
def e_form():
    global next_invoice_number

    form_data = DataEntry()
    address_list = CEntry.query.all()
    parts = PEntry.query.all()
    
    err_msg = ""
  
    if request.method == "POST":
        print('='*100, request.form, )
        global LASTENTRY
        global e_form_note
        global PartID_for_e_form
         # setting part price
        

        try:
            customer = request.json['customer']['id']
            order = request.json['order']
            order_cnt = 0
            DEntry_cnt = 0
            order_len = len(order)
            print(' 1 ->'*10,'in try block')
            if customer and order:
                
                next_invoice_number = generate_next_invoice_number()
                new_invoice = Invoice(invoice_number=next_invoice_number)
                
                for item in order:
                    print(' 3 ->'*10,'in for block')

                    part = PEntry.query.filter_by(part_id=item[1]).first()
                    if part.container_qty > 0 or part.pieces_qty > 0:
                        # Update inventory quantities
                        part.container_qty -= item[3]
                        part.pieces_qty -= item[4]
                        # Commit changes to the database
                        db.session.commit()
                        order_cnt += 1
                        print(' 4 ->'*10,'in CTN PCs update block', order_cnt)

                    else:
                        return jsonify({'error': str(e)}), 400
                    
                    data = DEntry(
                        part_id=item[1],
                        container_qty=item[3],
                        pieces_qty=item[4],
                        price=item[6],
                        cust_id=customer,
                        invoice_no=next_invoice_number
                        # time=datetime.strptime(datetime.datetime.now().strftime('%d-%m-%Y ~ %H:%M'), '%d-%m-%Y ~ %H:%M')
                    )
                    db.session.add(data)
                    db.session.commit()
                    DEntry_cnt += 1
                    print(' 5 ->'*10,'in DEntry update block', DEntry_cnt)

                if order_cnt == order_len and DEntry_cnt == order_len:
                    print(' 6 ->'*10,'in CTN PCs update block', ( order_cnt == order_len), (DEntry_cnt == order_len))
                    db.session.add(new_invoice)
                    db.session.commit()
                    
                    return jsonify({'Success': 'Transaction successful'}), 200
                
        except Exception as e:
            print(' 7 ->', 'In exception ', str(e))
            return jsonify({'error': str(e)}), 400
        
    return render_template('sales/eform.html', form=form_data, name_list=address_list, part_list=parts, 
                           address_list=address_list,
                           lastentry=LASTENTRY, e_form_note=e_form_note, err_msg=err_msg)

@sales_bp.route('/revieworder', methods=['GET'])
def revieworder():
    return render_template('sales/revieworder.html')

@sales_bp.route('/get_capacity', methods=['GET','POST'])
def get_capacity():
    capacity = PEntry.query.all()
    res = {}
    for c in capacity:
        res[c.part_id]=c.container_capacity
    response_data = {'cap' : res}
    return jsonify(response_data)



 # Function to generate the next invoice number
def generate_next_invoice_number():
    last_invoice = Invoice.query.order_by(Invoice.id.desc()).first()
    if last_invoice:
        last_invoice_number = int(last_invoice.invoice_number[3:])  # Extract the numeric part
        next_invoice_number = last_invoice_number + 1
    else:
        next_invoice_number = 1
    return f"INV{next_invoice_number:06d}"  # Format the next invoice number with leading zeros


@sales_bp.route('/prevbal_for_print', methods=['GET', 'POST'])
def prevbal_for_print():
    if request.json:
        totalbal = 0
        cust_id = request.json
        customer_info = DEntry.query.filter_by(cust_id=cust_id).all()
        for item in customer_info:
            totalbal += item.price

    return jsonify({'prevbal': totalbal}), 200



@sales_bp.route('/get_customers', methods=['GET','POST'])
def get_customers():
    # Assuming you have a function to fetch the customer data from your database
    customers = db.session.query(CEntry).order_by(func.lower(CEntry.name)).all()  # Implement this function
    customer_list = [{'id': customer.cust_id, 'name': customer.name, 'address': customer.address, 'contact': customer.contact} for customer in customers]

    print("visited", customer_list)
    response_data = {'cust': customer_list}

    return jsonify(response_data)


@sales_bp.route('/printinvoice', methods=['GET'])
def print_func():
    global next_invoice_number
    return render_template('sales/print.html', invoice=next_invoice_number)



@sales_bp.route('/get_parts', methods=['GET','POST'])
def get_parts():
    # Assuming you have a function to fetch the customer data from your database
    parts = db.session.query(PEntry).order_by(func.lower(PEntry.name)).all()  # Implement this function
    parts_list = [{'id': part.part_id, 'name': part.name, 'CTN': part.container_qty, 'PCS': part.pieces_qty, 'price': part.price} for part in parts]

    print("visited", parts_list)
    response_data = {'partlist': parts_list}

    return jsonify(response_data)

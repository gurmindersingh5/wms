from flask import Blueprint, request, render_template, redirect, url_for, session
from sqlalchemy import func

from ...models import PEntry
from ... import db

inventory_bp = Blueprint('inventory', __name__, template_folder='templates')

success_note = ""
@inventory_bp.route('/inventory', methods=['GET', 'POST'])
def inventory():
    print('inventory','#'*199, request.method , request.form.get('redirect_val'))
    Query = db.session.query(PEntry)
    results = Query.order_by(func.lower(PEntry.name)).all()
    # if request.method == "GET":
    #     if request.args.get('sort') == 'name':
    #         results = Query.order_by(func.lower(PEntry.name)).all()
    #     else:
    #         results = Query.all()
    NOTE = ""
    
    print(request.method, request.args, request.args.get('sort'))
    # print([result.container_qty for result in results])
    if request.method == "POST":
        if 'name' in request.form:
            name_query = request.form['name']
            if name_query:
                results = Query.filter(PEntry.name.like(f"%{name_query}%")).all()
                if not results:
                    NOTE = "Not found in database"
                else:
                    NOTE = f"{len(results)} entry/ies found"
        if request.form.get('redirect_val') == 'add_p':
            return redirect(url_for('inventory.redirect_p_form'))
        if request.form.get('redirect_val') == 'edit_p':
            return redirect(url_for('inventory.redirect_edit_p'))

    return render_template('inventory/inventory.html', results=results, note=NOTE)

@inventory_bp.route('/redirect_pform', methods=['GET', 'POST'])
def redirect_p_form():
    try:
        if not "user_id" in session:
            return redirect(url_for('login.login'))
        else:
            return redirect(url_for('addproduct.p_form'))
    except:
        pass
    return render_template('inventory/redirect_pform.html')




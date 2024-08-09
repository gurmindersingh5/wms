from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required

from ...models import PEntry
from ... import db

editproduct_bp = Blueprint('editproduct', __name__, template_folder='templates')


PartID = None  
@editproduct_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_p():
    # if not "user_id" in session:
    #     return redirect(url_for('login.login'))
    
    Query = db.session.query(PEntry)
    results = Query.order_by(func.lower(PEntry.name)).all()
    NOTE = ""

    if request.method == "POST":
        try:
            if request.get_json:
                global PartID
                PartID = request.get_json()['part_id']
                return redirect(url_for('editproduct.detailed_edit_p'))
        except:
            pass
        
        try:
            if 'name' in request.form:
                name_query = request.form['name']
                print('name_query: ', name_query)
                if name_query:
                    results = Query.filter(PEntry.name.like(f"%{name_query}%")).all()
                    if not results:
                        NOTE = "Not found in database"
                    else:
                        NOTE = f"{len(results)} entry/ies found"
                       

        except Exception as e:
            # Handle specific exceptions if needed or log the exception for debugging
            print(f"An error occurred: {e}")
        print('request.get_json: ', request.get_json, 'request.form[name]: ',  request.form, '0'*10)
    
    return render_template('editproduct/edit.html', results=results, note=NOTE)


@editproduct_bp.route('/detailed', methods=['GET', 'POST'])
@login_required
def detailed_edit_p():
    global PartID
    data = db.session.query(PEntry).filter_by(part_id=PartID).first()
    if request.method == 'POST':
        
        try:
            if request.json['updated_data']:
                recieve_updated_data = request.json['updated_data']
                data_to_be_edited = db.session.query(PEntry).filter_by(part_id=recieve_updated_data[0]).first()
                if data_to_be_edited and len(recieve_updated_data) == 6:
                    data_to_be_edited.name = str(recieve_updated_data[1])
                    data_to_be_edited.container_qty = int(recieve_updated_data[2])
                    data_to_be_edited.pieces_qty = int(recieve_updated_data[3])
                    data_to_be_edited.price = float(recieve_updated_data[4])
                    data_to_be_edited.container_capacity = int(recieve_updated_data[5])
                    try:
                        db.session.commit()
                        print('succesfully committed----')
                        return 'committed', 200
                    except SQLAlchemyError as e:
                        db.session.rollback()  # Rollback changes if an error occurs
                        error_message = str(e)  # Get the error message
                        print(error_message, 'error')
                        return render_template('editproduct/detailed.html', error_message=error_message, data=data)
                    finally:
                        db.session.close()  # Close the session
        except:
            pass        
        # if statement to delete the data to be deleted
        try:
            if request.get_json()['delete'] == "true":
                entry_to_delete = PEntry.query.filter_by(part_id=PartID).first()
                if entry_to_delete:
                    db.session.delete(entry_to_delete)
                    db.session.commit()
                    return 'Deletion committed', 200
                else:
                    return jsonify({'error':'Row not found'})
        except Exception as e:
            print('error', str(e))        
    return render_template('editproduct/detailed.html', data=data)



@editproduct_bp.route('/redirect_editp', methods=['GET', 'POST'])
def redirect_edit_p():
    try:
        if not "user_id" in session:
            return redirect(url_for('login_edit_p'))
        else:
            return redirect(url_for('edit_p'))
    except:
        pass
    return render_template('inventory/redirect_editp.html')


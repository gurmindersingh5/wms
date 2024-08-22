from ..models import Visits
from .. import db
from sqlalchemy import distinct


def save_ip_addr(ip):
    """
    Save the ip addresses in the db to maintain visitor count.

    param: ip: ip address from request.remote_addr
    returns: status code 200
    """
    if len(ip.split('.')) == 4:
        if not Visits.query.filter_by(ip_addr=ip).first():    
            try:
                data = Visits(ip_addr=ip)
                db.session.add(data)
                db.session.commit()
                return {'status': 200}
            except Exception as e:
                db.session.rollback()  
                return {'status': 500, 'error': str(e)}
        return {'status': 400}
    else:
        return {'status': 400}


def visitor_counter_func():
    """
    Counts the total number of visitors (total number of unique ip addresses)

    returns: unique ip addresses' count
    """

    # Count unique IP addresses
    unique_ip_addresses = db.session.query(Visits.ip_addr).all()
    unique_visitors = len(unique_ip_addresses)

    return unique_visitors

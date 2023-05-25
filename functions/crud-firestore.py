import functions_framework
import firebase_admin
from firebase_admin import firestore

app = firebase_admin.initialize_app()
db = firestore.client()

@functions_framework.http
def crud_tickets(request):
    if request.method == 'GET':
        data_list = []
        ticket_id = request.args.get('ticket_id')
        doc_ref = db.collection('customer_bot').where('ticket_id', '==', ticket_id)
        results = doc_ref.get()
        
        for doc in results:
            data = doc.to_dict()
            data_list.append(data)

        return data_list

    elif request.method == 'PUT':
        data = request.get_json()
        ticket_id = data['ticket_id']
        doc_ref = db.collection('customer_bot').where('ticket_id', '==', ticket_id)
        results = doc_ref.stream()

        for doc in results:
            doc.reference.update(data)
    
        return 'TICKET UPDATED'

    elif request.method == 'DELETE':
        ticket_id = request.args.get('ticket_id')
        doc_ref = db.collection('customer_bot').where('ticket_id', '==', ticket_id)
        results = doc_ref.stream()

        for doc in results:
            doc.reference.delete()

        return 'TICKET DELETED'

    else:
        return 'INVALID REQUEST'

import logging
from google.cloud import firestore
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gkey.json"
    db = firestore.Client()
    logging.info('firestore client')    
    print('db')

    users_ref = db.collection(u'queries').order_by(u'date', direction=firestore.Query.DESCENDING).limit(max)
    for doc in users_ref.stream():
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
    print('ref')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )

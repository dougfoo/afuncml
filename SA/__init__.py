import logging
import json
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import requests
import azure.functions as func
# from google.cloud import firestore


def main(req: func.HttpRequest) -> func.HttpResponse:
    print('main start')
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gkey.json"
    # db = firestore.Client()
    # print('db')

    # users_ref = db.collection(u'queries').order_by(u'date', direction=firestore.Query.DESCENDING).limit(max)
    # for doc in users_ref.stream():
    #     print(u'{} => {}'.format(doc.id, doc.to_dict()))
    # print('ref')

    data = req.params.get('data')
    model = req.params.get('model')
    if not model:
        model = 'all'
    if not data:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            data = req_body.get('data')

    if data:
        resp = sa_predict(model=model, sentence=data)
        return func.HttpResponse(body=resp, headers={"content-type": "application/json"})
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )

# NLP sentiment analysis section
# merge to common format:
#  {
#    "input": "I love the world so much",
#    "results": [
#       {
#        "model": "AzureML",
#        "nScore": 0.8,  # -1.0 to +1.0 w/ 1.0 being positive, -1.0 negative, 0.0 neutral
#        "rScore": .5,  # raw results in case it is -0.5 to 0.5 or -1 to +1
#        "extra": "na optional text only"#
#       },
#       ...
#     ]
#  }


def sa_predict(model='all',sentence='default sentence'):
	print(sentence)

	resp = {}
	resp['input'] = sentence
	resp['results'] = []

	if (model == 'all'):
		resp['results'].append(vader(sentence))
		resp['results'].append(textblob(sentence))
		resp['results'].append(azure_sentiment(sentence))
		resp['results'].append(gcp_sentiment(sentence))
	elif (model == 'azure'):
		resp['results'] = azure_sentiment(sentence)
	elif (model == 'vader'):
		resp['results'] = vader(sentence)
	elif (model == 'textblob'):
		resp['results'] = textblob(sentence)
	elif (model == 'google'):
		resp['results'] = gcp_sentiment(sentence)
	else:
		# flag error 
		return 'No Model exists for '+model
	return json.dumps(resp)


def textblob(sentence):
	resp = {}
	resp['model'] = 'TextBlob'
	resp['extra'] = 'models returns -1 to +1'
	resp['url'] = 'https://textblob.readthedocs.io/en/dev/'
	# create TextBlob object of passed tweet text
	analysis = TextBlob(sentence)
	resp['rScore'] = analysis.sentiment.polarity
	resp['nScore'] = analysis.sentiment.polarity
	# set sentiment
	return resp


def vader(sentence):
	resp = {}
	resp['model'] = 'Vader'
	resp['extra'] = 'model returns -1 to +1'
	resp['url'] = 'https://pypi.org/project/vaderSentiment/'
	analyser = SentimentIntensityAnalyzer()
	score = analyser.polarity_scores(sentence)['compound'] 
	resp['rScore'] = score
	resp['nScore'] = score
	return resp


# azure and google inspired from:  https://www.pingshiuanchua.com/blog/post/simple-sentiment-analysis-python?utm_campaign=News&utm_medium=Community&utm_source=DataCamp.com
##
def gcp_sentiment(text):
	resp = {}
	resp['model'] = 'Google NLP'
	resp['extra'] = 'model returns -1 to +1'
	resp['url'] = 'https://cloud.google.com/natural-language/'

	gcp_url = "https://language.googleapis.com/v1/documents:analyzeSentiment?key=AIzaSyBN-SLv7YPAMARDo2eQl7Y_yyy84xpWcHU"

	document = {'document': {'type': 'PLAIN_TEXT', 'content': text}, 'encodingType':'UTF8'}
	response = requests.post(gcp_url, json=document)
	sentiments = response.json()
	score = sentiments['documentSentiment']['score']

	resp['rScore'] = score
	resp['nScore'] = score 
	return resp


# azure service calls
##
def azure_sentiment(text):
	resp = {}
	resp['model'] = 'Azure NLP'
	resp['extra'] = 'model returns 0 to 1'
	resp['url'] = 'https://azure.microsoft.com/en-us/services/cognitive-services/text-analytics/'

	documents = {'documents': [
		{'id': '1', 'text': text}
	]}

	azure_key = 'd6c00eb74e58455187125aa6a97fd976'  # Update here
	azure_endpoint = 'https://textsentimentanalyzer.cognitiveservices.azure.com/text/analytics/v2.1/'
	sentiment_azure = azure_endpoint + '/sentiment'

	headers = {"Ocp-Apim-Subscription-Key": azure_key}
	response = requests.post(sentiment_azure, headers=headers, json=documents)
	score = response.json()['documents'][0]['score']

	resp['rScore'] = score
	resp['nScore'] = 2 * (score - 0.5) 

	return resp


# all from scratch
#   - tokenize
#   - general cleanup
#   - stem
#   - lemmitize
#   - stopwords
#   - pos tagging ? (spacy)
#   - named entity recognition (NER) -- not needed
#   - word vector ?
#   - sa lexicon ?  stanford?  which ?
###
def custom_nlp(text):
	return None


# bert on azure (costly)
## 
def bert(text):
	return None


import logging
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
import numpy as np
import requests


import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    sentence = req.params.get('data')
    if not sentence:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            sentence = req_body.get('sentence')

    if sentence:
        return func.HttpResponse(f"Hello {sentence}!")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )


def sa_predict(model='all', sentence='test sentence'):
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

from google.cloud import language_v1
from google.cloud.language_v1 import enums
import six


def sample_analyze_sentiment(content):

    client = language_v1.LanguageServiceClient()

    # content = 'Your text to analyze, e.g. Hello, world!'

    if isinstance(content, six.binary_type):
        content = content.decode('utf-8')

    type_ = enums.Document.Type.PLAIN_TEXT
    document = {'type': type_, 'content': content}

    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment
    print('Score: {}'.format(sentiment.score))
    print('Magnitude: {}'.format(sentiment.magnitude))



def make_input_utf(func):
	def internal(self, text):
		if isinstance(text, six.binary_type):
			text = text.decode('utf-8')
		return func(self, text)	
	return internal

class GoogleNLP:
	def __init__(self):
		self.client = language_v1.LanguageServiceClient()

	def __enter__(self):
		return self

	def __exit__(self, *exc):
		if any(exc):
			for x in exc:
				print(exc)
	@make_utf
	def analyze(self, text):
		doc = dict(
			type=enums.Document.Type.PLAIN_TEXT,
			content=text
			)
		response = client.analyze_sentiment(document)
    		sentiment = response.document_sentiment
    		
		print('Score: {}'.format(sentiment.score))
    		print('Magnitude: {}'.format(sentiment.magnitude))
		
		return sentiment

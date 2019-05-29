from srec_nlp.common import NLP, Query
from google.cloud import language_v1
from google.cloud.language_v1 import enums
import six


@NLP
class GoogleNLP:
    """
	Example usage:

	with GoogleNLP() as nlp:
		query = nlp.analyze('foo is bar')

	---
	nlp = GoogleNLP()
	query = nlp.analyze('foo is bar')

	"""

    def __init__(self):
        self.client = language_v1.LanguageServiceClient()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        if any(exc):
            for x in exc:
                print(exc)

    def analyze(self, text, log=False) -> Query:
        print(self)
        doc = dict(type=enums.Document.Type.PLAIN_TEXT, content=text)
        response = self.client.analyze_sentiment(doc)
        sentiment = response.document_sentiment
        log and print(f"Score: {sentiment.score}")
        log and print(f"Magnitude: {sentiment.magnitude}")
        result = Query(
            [
                Query(sentence.content, sentence.score)
                for sentence in response.sentences
            ],
            sentiment.score,
        )
        return result



@NLP
class foonlp:
    def analyze(self, text):
        return Query('foo', 12)
    pass


foonlp().analyze("foo")


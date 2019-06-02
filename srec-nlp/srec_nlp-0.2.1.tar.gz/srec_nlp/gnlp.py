from srec_nlp.common import _ensure_utf, Query
from google.cloud import language_v1
from google.cloud.language_v1 import enums
from pathlib import Path
from typing import Union
import os
import six

_env_credentials = "GOOGLE_APPLICATION_CREDENTIALS"


class GoogleNLP:

    def __init__(self):
        self.client = language_v1.LanguageServiceClient()
        return self

    @classmethod
    def using_credentials(cls, credentials: Union[Path, str]):
        """
        Note: Using the function sets the environment variable 'GOOGLE_APPLICATION_CREDENTIALS'.

        If you have that set then use GoogleNLP(), if you've already used using_credentials once,
        you don't need to use it again.
        """
        if _env_credentials in os.environ:
            return cls()

        credentials = Path(credentials)
        assert credentials.is_file(), f"Path: {credentials} does not exist."
        os.environ[_env_credentials] = str(credentials)
        return cls()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        if any(exc):
            for x in exc:
                print(exc)

    @_ensure_utf
    def sentiment(self, text) -> Query:
        doc = dict(type=enums.Document.Type.PLAIN_TEXT, content=text)
        response = self.client.analyze_sentiment(doc)
        sentiment = response.document_sentiment
        result = Query(
            [
                Query(sentence.content, sentence.score)
                for sentence in response.sentences
            ],
            sentiment.score,
        )
        return result

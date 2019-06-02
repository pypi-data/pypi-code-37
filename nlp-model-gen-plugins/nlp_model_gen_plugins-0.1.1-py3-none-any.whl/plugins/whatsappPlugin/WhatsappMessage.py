# @Constants
from nlp_model_gen_plugins.constants import TASK_STATUS_FINISHED

class WhatsappMessage:
    def __init__(self, filename, origin, timestamp, content, nlp_admin_instance, analysis_task_id):
        self.__filename = filename
        self.__from = origin
        self.__content = content
        self.__timestamp = timestamp
        self.__nlp_admin_instance = nlp_admin_instance
        self.__analysis_task_id = analysis_task_id
        self.__analyzed = False
        self.__analysis_result = dict({})
        self.__token_frequency = dict({})

    def __build_results_dict(self, results):
        return [result.to_dict() for result in results]

    def get_token_frequency(self):
        return self.__token_frequency

    def is_analyzed(self):
        if not self.__analyzed:
            self.check_analysis_task()
        return self.__analyzed

    def check_analysis_task(self):
        if not self.__nlp_admin_instance or self.__analyzed:
            return
        taks_status = self.__nlp_admin_instance.get_task_status(self.__analysis_task_id)['resource']
        if taks_status['status'] == TASK_STATUS_FINISHED:
            self.__analyzed = True
            if taks_status['error']['active']:
                self.__analysis_result = {
                    'error': True,
                    'ner_results': [],
                    'tokenizer_results': [],
                    'token_frequency': {}
                }
            else:
                self.__analysis_result = {
                    'error': False,
                    'ner_results': self.__build_results_dict(taks_status['results']['ner_results']),
                    'tokenizer_results': self.__build_results_dict(taks_status['results']['tokenizer_results']),
                    'tokenizer_positive': len(taks_status['results']['tokenizer_results']) > 0,
                    'ner_positive': len(taks_status['results']['ner_results']) > 0
                }
                self.__token_frequency = taks_status['results']['token_frequency']

    def to_dict(self):
        return {
            'filename': self.__filename,
            'from': self.__from,
            'timestamp': self.__timestamp,
            'content': self.__content,
            'analysis_task_id': self.__analysis_task_id,
            'analysis_result': self.__analysis_result
        }

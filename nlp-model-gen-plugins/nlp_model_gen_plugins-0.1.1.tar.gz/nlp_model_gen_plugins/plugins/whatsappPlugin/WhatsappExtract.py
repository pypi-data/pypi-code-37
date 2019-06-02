"""
nlp_model_gen plugin for formatting whatsapp extracted data.

Expected format:
    De: From: 5492231111111@s.whatsapp.net Persona1
    Marca de hora: 23/11/2017 22:53:55(UTC-3)
    Aplicación de origen: WhatsApp
    Contenido:
    Hola Ana
    -----------------------------

"""

# @Constants
from nlp_model_gen_plugins.constants import (
    WHATSAPP_DIVIDER,
    WHATSAPP_FROM,
    WHATSAPP_INLINE_DIVIDER,
    WHATSAPP_TIMESTAMP
)

# @utils
from nlp_model_gen_plugins.utils.collectionsUtils import tuple_word_list_to_counter

# @Classes
from .WhatsappMessage import WhatsappMessage

class WhatsappExtract:
    def __init__(self, files, nlp_admin_instance=None, model_id=''):
        self.__extracts_list = []
        self.__nlp_admin_instance = nlp_admin_instance
        self.__model_id = model_id
        self.__initialize(files)

    def __get_message_field(self, message_parts, field):
        for part in message_parts:
            if part.startswith(field):
                return part.replace(field, '')
        return ''

    def __analyze_message(self, content):
        if not self.__nlp_admin_instance:
            return None
        return self.__nlp_admin_instance.analyze_text(self.__model_id, content, True)

    def __process_file(self, file):
        messages_data = file.read()
        for message in messages_data.split(WHATSAPP_DIVIDER):
            message_parts = message.split(WHATSAPP_INLINE_DIVIDER)
            part_from = self.__get_message_field(message_parts, WHATSAPP_FROM)
            part_timestamp = self.__get_message_field(message_parts, WHATSAPP_TIMESTAMP)
            part_content = message_parts[len(message_parts) - 2]
            analysis_task = self.__analyze_message(part_content)['resource']['task_id']
            self.__extracts_list.append(WhatsappMessage(
                file.name,
                part_from,
                part_timestamp,
                part_content,
                self.__nlp_admin_instance,
                analysis_task
            ))

    def __initialize(self, files):
        for file in files:
            self.__process_file(file)

    def get_extracts_list(self):
        if not self.is_analysed():
            return None
        return [message.to_dict() for message in self.__extracts_list]

    def get_ner_positives(self):
        if not self.is_analysed():
            return None
        return [message.to_dict() for message in self.__extracts_list if message.to_dict()['analysis_result']['ner_positive']]

    def get_tokenizer_positives(self):
        if not self.is_analysed():
            return None
        return [message.to_dict() for message in self.__extracts_list if message.to_dict()['analysis_result']['tokenizer_positive']]

    def get_positives_results(self):
        if not self.is_analysed():
            return None
        return [message.to_dict() for message in self.__extracts_list if message.to_dict()['analysis_result']['ner_positive'] or message.to_dict()['analysis_result']['tokenizer_positive']]
    
    def get_token_frequency(self):
        if not self.is_analysed():
            return None
        frequency_counter = dict({})
        for message in self.__extracts_list:
            token_frequency = message.get_token_frequency()
            for key in token_frequency.keys():
                token_count = tuple_word_list_to_counter(token_frequency[key])
                if key in frequency_counter.keys():
                    frequency_counter[key] = frequency_counter[key] + token_count
                else:
                    frequency_counter[key] = token_count
        count_results = dict({})
        for key in frequency_counter.keys():
            count_results[key] = frequency_counter[key].most_common()
        return count_results

    def is_analysed(self):
        if not self.__nlp_admin_instance:
            return False
        for extract in self.__extracts_list:
            if not extract.is_analyzed():
                return False
        return True

from edc_model_wrapper import ModelWrapper


class AeInitialModelWrapper(ModelWrapper):
    next_url_name = "ae_listboard_url"
    model = "ambition_ae.aeinitial"
    next_url_attrs = ["subject_identifier"]

    @property
    def pk(self):
        return str(self.object.pk)

    @property
    def subject_identifier(self):
        return self.object.subject_identifier

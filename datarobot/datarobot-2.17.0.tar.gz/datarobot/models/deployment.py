from collections import defaultdict

import dateutil
import trafaret as t

from datarobot.models.api_object import APIObject
from ..utils import encode_utf8_if_py2, get_id_from_location, from_api
from ..utils.pagination import unpaginate
from ..utils.waiters import wait_for_async_resolution


class Deployment(APIObject):
    """A deployment created from a DataRobot model.

    Attributes
    ----------
    id : str
        the id of the deployment
    label : str
        the label of the deployment
    description : str
        the description of the deployment
    default_prediction_server : dict
        information on the default prediction server of the deployment
    model : dict
        information on the model of the deployment
    capabilities : dict
        information on the capabilities of the deployment
    prediction_usage : dict
        information on the prediction usage of the deployment
    service_health : dict
        information on the service health of the deployment
    model_health : dict
        information on the model health of the deployment
    accuracy_health : dict
        information on the accuracy health of the deployment
    """

    _path = 'deployments/'
    _default_prediction_server_converter = t.Dict({
        t.Key('id'): t.String(),
        t.Key('url', optional=True): t.String(allow_blank=True),
        t.Key('datarobot-key', optional=True): t.String(allow_blank=True),
    }).allow_extra('*')
    _model_converter = t.Dict({
        t.Key('id', optional=True): t.String(),
        t.Key('type', optional=True): t.String(allow_blank=True),
        t.Key('target_name', optional=True): t.String(allow_blank=True),
        t.Key('project_id', optional=True): t.String(allow_blank=True),
    }).allow_extra('*')
    _capabilities = t.Dict({
        t.Key('supports_drift_tracking', optional=True): t.Bool(),
        t.Key('supports_model_replacement', optional=True): t.Bool(),
    }).allow_extra('*')
    _prediction_usage = t.Dict({
        t.Key('daily_rates', optional=True): t.List(t.Float()),
        t.Key('last_timestamp', optional=True): t.String >> (lambda s: dateutil.parser.parse(s))
    }).allow_extra('*')
    _health = t.Dict({
        t.Key('status', optional=True): t.String(allow_blank=True),
        t.Key('start_date', optional=True): t.String >> (lambda s: dateutil.parser.parse(s)),
        t.Key('end_date', optional=True): t.String >> (lambda s: dateutil.parser.parse(s)),
    }).allow_extra('*')
    _converter = t.Dict({
        t.Key('id'): t.String(),
        t.Key('label', optional=True): t.String(allow_blank=True),
        t.Key('description', optional=True): t.String(allow_blank=True) | t.Null(),
        t.Key('default_prediction_server', optional=True): _default_prediction_server_converter,
        t.Key('model', optional=True): _model_converter,
        t.Key('capabilities', optional=True): _capabilities,
        t.Key('prediction_usage', optional=True): _prediction_usage,
        t.Key('service_health', optional=True): _health,
        t.Key('model_health', optional=True): _health,
        t.Key('accuracy_health', optional=True): _health,
    }).allow_extra('*')

    def __init__(self, id=None, label=None, description=None, default_prediction_server=None,
                 model=None, capabilities=None, prediction_usage=None, service_health=None,
                 model_health=None, accuracy_health=None):
        self.id = id
        self.label = label
        self.description = description
        self.default_prediction_server = default_prediction_server
        self.model = model
        self.capabilities = capabilities
        self.prediction_usage = prediction_usage
        self.service_health = service_health
        self.model_health = model_health
        self.accuracy_health = accuracy_health

    def __repr__(self):
        return encode_utf8_if_py2(u'{}({})'.format(self.__class__.__name__, self.label or self.id))

    @classmethod
    def create_from_learning_model(cls, model_id, label, description=None,
                                   default_prediction_server_id=None):
        """Create a deployment from a DataRobot model.

        .. versionadded:: v2.17

        Parameters
        ----------
        model_id : str
            id of the DataRobot model to deploy
        label : str
            a human readable label of the deployment
        description : str, optional
            a human readable description of the deployment
        default_prediction_server_id : str
            an identifier of a prediction server to be used as the default prediction server

        Returns
        -------
        deployment : Deployment
            The created deployment

        Examples
        --------
        .. code-block:: python

            from datarobot import Project, Deployment
            project = Project.get('5506fcd38bd88f5953219da0')
            model = project.get_models()[0]
            deployment = Deployment.create_from_learning_model(model.id, 'New Deployment')
            deployment
            >>> Deployment('New Deployment')
        """

        payload = {'model_id': model_id, 'label': label, 'description': description}
        if default_prediction_server_id:
            payload['default_prediction_server_id'] = default_prediction_server_id

        url = '{}fromLearningModel/'.format(cls._path)
        deployment_id = cls._client.post(url, data=payload).json()['id']
        return cls.get(deployment_id)

    @classmethod
    def list(cls):
        """List all deployments a user can view.

        .. versionadded:: v2.17

        Returns
        -------
        deployments : list
            a list of deployments the user can view

        Examples
        --------
        .. code-block:: python

            from datarobot import Deployment
            deployments = Deployment.list()
            deployments
            >>> [Deployment('New Deployment'), Deployment('Previous Deployment')]
        """

        data = unpaginate(cls._path, {}, cls._client)
        return [cls.from_server_data(item) for item in data]

    @classmethod
    def get(cls, deployment_id):
        """Get information about a deployment.

        .. versionadded:: v2.17

        Parameters
        ----------
        deployment_id : str
            the id of the deployment

        Returns
        -------
        deployment : Deployment
            the queried deployment

        Examples
        --------
        .. code-block:: python

            from datarobot import Deployment
            deployment = Deployment.get(deployment_id='5c939e08962d741e34f609f0')
            deployment.id
            >>>'5c939e08962d741e34f609f0'
            deployment.label
            >>>'New Deployment'
        """

        path = '{}{}/'.format(cls._path, deployment_id)
        return cls.from_location(path)

    def delete(self):
        """
        Delete this deployment.

        .. versionadded:: v2.17
        """

        url = '{}{}/'.format(self._path, self.id)
        self._client.delete(url)

    def replace_model(self, new_model_id, reason):
        """
        Replace the model used in this deployment. To confirm model replacement eligibility, use
        :meth:`~datarobot.Deployment.validate_replacement_model` beforehand.

        .. versionadded:: v2.17

        Model replacement is an asynchronous process, which means some preparatory work may
        be performed after the initial request is completed. This function will not return until all
        preparatory work is fully finished.

        Predictions made against this deployment will start using the new model as soon as the
        initial request is completed. There will be no interruption for predictions throughout
        the process.

        Parameters
        ----------
        new_model_id : str
            The id of the new model to use
        reason : MODEL_REPLACEMENT_REASON
            The reason for the model replacement. Must be one of 'ACCURACY', 'DATA_DRIFT', 'ERRORS',
            'SCHEDULED_REFRESH', 'SCORING_SPEED', or 'OTHER'. This value will be stored in the model
            history to keep track of why a model was replaced

        Examples
        --------
        .. code-block:: python

            from datarobot import Deployment
            deployment = Deployment.get(deployment_id='5c939e08962d741e34f609f0')
            deployment.model['id'], deployment.model['type']
            >>>('5c0a979859b00004ba52e431', 'Decision Tree Classifier (Gini)')

            deployment.replace_model('5c0a969859b00004ba52e41b', MODEL_REPLACEMENT_REASON.ACCURACY)
            deployment.model['id'], deployment.model['type']
            >>>('5c0a969859b00004ba52e41b', 'Support Vector Classifier (Linear Kernel)')
        """

        url = '{}{}/model/'.format(self._path, self.id)
        payload = {'modelId': new_model_id, 'reason': reason}
        response = self._client.patch(url, data=payload)
        deployment_loc = wait_for_async_resolution(self._client, response.headers['Location'])
        deployment_id = get_id_from_location(deployment_loc)
        deployment = Deployment.get(deployment_id)
        self.model = deployment.model

    def validate_replacement_model(self, new_model_id):
        """Validate a model can be used as the replacement model of the deployment.

        .. versionadded:: v2.17

        Parameters
        ----------
        new_model_id : str
            the id of the new model to validate

        Returns
        -------
        status : str
            status of the validation, will be one of 'passing', 'warning' or 'failing'.
            If the status is passing or warning, use :meth:`~datarobot.Deployment.replace_model` to
            perform a model replacement. If the status is failing, refer to ``checks`` for more
            detail on why the new model cannot be used as a replacement.
        message : str
            message for the validation result
        checks : dict
            explain why the new model can or cannot replace the deployment's current model
        """

        url = '{}{}/model/validation/'.format(self._path, self.id)
        payload = {'modelId': new_model_id}
        data = from_api(self._client.post(url, data=payload).json())
        return data.get('status'), data.get('message'), data.get('checks')

    def get_drift_tracking_settings(self):
        """Retrieve drift tracking settings of this deployment.

        .. versionadded:: v2.17

        Returns
        -------
        settings : dict
            Drift tracking settings of the deployment containing two nested dicts with key
            ``target_drift`` and ``feature_drift``, which are further described below.

            ``Target drift`` setting contains:

            enabled : bool
                If target drift tracking is enabled for this deployment. To create or update
                existing ''target_drift'' settings, see
                :meth:`~datarobot.Deployment.update_drift_tracking_settings`

            ``Feature drift`` setting contains:

            enabled : bool
                If feature drift tracking is enabled for this deployment. To create or update
                existing ''feature_drift'' settings, see
                :meth:`~datarobot.Deployment.update_drift_tracking_settings`
        """

        url = '{}{}/settings/'.format(self._path, self.id)
        response_json = from_api(self._client.get(url).json())
        return {key: value for key, value in response_json.items()
                if key in ['target_drift', 'feature_drift']}

    def update_drift_tracking_settings(self, target_drift_enabled=None, feature_drift_enabled=None):
        """Update drift tracking settings of this deployment.

        .. versionadded:: v2.17

        Updating drift tracking setting is an asynchronous process, which means some preparatory
        work may be performed after the initial request is completed. This function will not return
        until all preparatory work is fully finished.

        Parameters
        ----------
        target_drift_enabled : bool, optional
            if target drift tracking is to be turned on
        feature_drift_enabled : bool, optional
            if feature drift tracking is to be turned on
        """

        payload = defaultdict(dict)
        if target_drift_enabled is not None:
            payload['targetDrift']['enabled'] = target_drift_enabled
        if feature_drift_enabled is not None:
            payload['featureDrift']['enabled'] = feature_drift_enabled
        if not payload:
            raise ValueError()

        url = '{}{}/settings/'.format(self._path, self.id)
        response = self._client.patch(url, data=payload)
        wait_for_async_resolution(self._client, response.headers['Location'])

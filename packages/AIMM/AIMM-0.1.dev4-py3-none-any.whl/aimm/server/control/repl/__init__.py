from hat import juggler
from hat import aio
import asyncio
import base64
import logging
import numpy
import pandas
import traceback

from aimm.server import common
from aimm import plugins


mlog = logging.getLogger(__name__)


async def create(conf, engine, async_group, _):
    common.json_schema_repo.validate(
        'aimm://server/control/repl/schema.yaml#', conf)
    control = REPLControl()

    srv_conf = conf['server']
    server = await juggler.listen(
        srv_conf['host'], srv_conf['port'], control._connection_cb,
        pem_file=srv_conf.get('pem_file'),
        autoflush_delay=srv_conf.get('autoflush_delay', 0.2),
        shutdown_timeout=srv_conf.get('shutdown_timeout', 0.1))

    _bind_resource(async_group, server)

    control._conf = conf
    control._engine = engine
    control._async_group = async_group
    control._server = server

    return control


class REPLControl(common.Control):

    @property
    def async_group(self) -> aio.Group:
        """Async group"""
        return self._async_group

    def _connection_cb(self, connection):
        session = Session(connection, self._engine, self._conf)
        self._async_group.spawn(aio.call_on_cancel, session.async_close)


class Session(aio.Resource):

    def __init__(self, connection, engine, conf):
        self._engine = engine
        self._user = None
        self._conf = conf

        self._connection = juggler.RpcConnection(connection, {
            'login': self._login,
            'logout': self._logout,
            'create_instance': self._create_instance,
            'add_instance': self._add_instance,
            'update_instance': self._update_instance,
            'fit': self._fit,
            'predict': self._predict})

    @property
    def async_group(self):
        return self._connection.async_group

    async def _run(self):
        await self._on_state_change()
        with self._engine.subscribe_to_state_change(
                lambda: self.async_group.spawn(self._on_state_change)):
            await self.async_group.wait_closing()

    async def _on_state_change(self):
        self._connection.set_local_data(
            await _state_to_json(self._engine.state))

    def _login(self, username, password):
        if {'username': username, 'password': password} in self._conf['users']:
            self._user = username
            self.async_group.spawn(self._run)
        else:
            asyncio.get_event_loop().call_later(1, self.close)
            raise Exception('login failed')

    def _logout(self):
        self._user = None

    async def _create_instance(self, model_type, args, kwargs):
        self._check_authorization()
        args = [_arg_from_json(a) for a in args]
        kwargs = {k: _arg_from_json(v) for k, v in kwargs.items()}

        task = self._engine.create_instance(model_type, *args, **kwargs)
        return await _model_to_json(await task)

    async def _add_instance(self, model_type, instance):
        self._check_authorization()
        instance = await _instance_from_json(instance, model_type)
        model = self._engine.add_instance(instance, model_type)
        return _model_to_json(model)

    async def _update_instance(self, model_type, instance_id, instance):
        self._check_authorization()
        model = common.Model(
            model_type=model_type,
            instance_id=instance_id,
            instance=await _instance_from_json(instance, model_type))
        await self._engine.update_instance(model)
        return await _model_to_json(model)

    async def _fit(self, instance_id, args, kwargs):
        self._check_authorization()
        args = [_arg_from_json(a) for a in args]
        kwargs = {k: _arg_from_json(v) for k, v in kwargs.items()}

        task = await self._engine.fit(instance_id, *args, **kwargs)
        return await _model_to_json(await task)

    async def _predict(self, instance_id, args, kwargs):
        self._check_authorization()
        args = [_arg_from_json(a) for a in args]
        kwargs = {k: _arg_from_json(v) for k, v in kwargs.items()}

        task = await self._engine.predict(instance_id, *args, **kwargs)
        return _prediction_to_json(await task)

    def _check_authorization(self):
        if self._user is None:
            raise Exception('unauthorized action')


async def _state_to_json(state):
    return {
        'models': {model_id: await _model_to_json(model)
                   for model_id, model in state['models'].items()},
        'actions': state['actions']}


async def _model_to_json(model):
    executor = aio.create_executor()
    instance_bytes = base64.b64encode(
        await executor(plugins.exec_serialize, model.model_type,
                       model.instance)).decode('utf-8')
    return {'instance_id': model.instance_id,
            'model_type': model.model_type,
            'instance': instance_bytes}


def _prediction_to_json(prediction):
    if isinstance(prediction, pandas.DataFrame):
        return {'type': 'pandas_dataframe',
                'data': prediction.to_dict()}
    if isinstance(prediction, pandas.Series):
        return {'type': 'pandas_series',
                'data': prediction.tolist()}
    if isinstance(prediction, numpy.ndarray):
        return {'type': 'numpy_array',
                'data': prediction.tolist()}
    return prediction


async def _instance_from_json(instance_b64, model_type):
    executor = aio.create_executor()
    return await executor(plugins.exec_deserialize, model_type,
                          base64.b64decode(instance_b64))


def _arg_from_json(arg):
    if not isinstance(arg, dict):
        return arg
    if arg.get('type') == 'data_access':
        return common.DataAccess(name=arg['name'],
                                 args=arg['args'],
                                 kwargs=arg['kwargs'])
    if arg.get('type') == 'numpy_array':
        return numpy.array(arg['data'], dtype=arg['dtype'])
    if arg.get('type') == 'pandas_dataframe':
        return pandas.DataFrame.from_dict(arg['data'])
    if arg.get('type') == 'pandas_series':
        return pandas.Series(arg['data'])
    return arg


def _exc_msg(e):
    return {'type': 'result', 'success': False, 'exception': str(e),
            'traceback': traceback.format_exc()}


def _bind_resource(async_group, resource):
    async_group.spawn(aio.call_on_cancel, resource.async_close)
    async_group.spawn(aio.call_on_done, resource.wait_closing(),
                      async_group.close)

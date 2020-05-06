from server.constants import MetricDataType, MetricStatus
import datetime


UPDATE_METRIC = {
    'description': dict(type='string', maxlength=100, default=''),
    'status': dict(type='integer', allowed=MetricStatus._ALL),
    'units': dict(type='string', maxlength=20, default='')
}

CREATE_METRIC = {
    'title': dict(type='string', required=True, minlength=3, maxlength=50),
    'uuid': dict(type='string', required=True, regex='^[a-z][a-z0-9_]*$', coerce=lambda s: s.lower()),
    'type': dict(type='integer', default=MetricDataType.FLOAT, allowed=MetricDataType._CERBERUS_ALLOWED)
}
CREATE_METRIC.update(UPDATE_METRIC)


PUSH_METRIC = {
    'value': dict(type=MetricDataType._CERBERUS_TYPES, required=True),
    'timestamp': dict(type='integer', rename='time'),
    'time': dict(type='datetime', coerce=datetime.datetime.utcfromtimestamp),
    'tag': dict(type='string')
}

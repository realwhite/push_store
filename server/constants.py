class MetricStatus:
    ACTIVE = 1
    PAUSED = 2

    _ALL = [ACTIVE, PAUSED]

    @classmethod
    def toggle_status(cls, current_status: int) -> int:
        if current_status == cls.ACTIVE:
            return cls.PAUSED

        return cls.ACTIVE


class MetricDataType:
    INT = 1
    FLOAT = 2
    STRING = 3
    INCREMENT = 4

    _CERBERUS_ALLOWED = set([INT, FLOAT, STRING, INCREMENT])

    __DB_TYPES_MAP = {
        # Postgres data types mapping
        INT: 'BIGINT',
        FLOAT: 'DOUBLE PRECISION',
        STRING: 'TEXT',
        INCREMENT: 'BIGINT'
    }

    __CERBERUS_TYPES_MAP = {
        # ('CERBERUS_TYPE_NAME', PYTHON_FUNC_FOR_COERCE)
        INT: ('integer', int),
        FLOAT: ('float', float),
        STRING: ('string', str),
        INCREMENT: ('integer', int)
    }

    _CERBERUS_TYPES = list({v[0] for v in __CERBERUS_TYPES_MAP.values()})

    @classmethod
    def get_db_type(cls, _type):
        return cls.__DB_TYPES_MAP.get(_type)

    @classmethod
    def get_cerberus_type(cls, _type):
        return cls.__CERBERUS_TYPES_MAP.get(_type)

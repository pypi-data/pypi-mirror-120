from .sessions import session_scope
from .utils import object_as_dict


def get_bulletin_by_range(engine, table, starttime, endtime, eventtype=None):
    """
    Get bulletin by particular time range and eventtype. If eventtype is None,
    query all events.

    :param engine: SQLAlchemy engine.

    :type engine: :class:`sqlalchemy.engine.base.Engine`

    :param table: SQLAlchemy model or table.

    :param starttime: Start time of the query.

    :type starttime: datetime.datetime

    :param endtime: End time of the query.

    :type endtime: datetime.datetime

    :param eventtype: Event type, e.g. VTA, VTB, MP. If you want to query
    multiple eventtypes, pass a list or tuple. If eventtype is None, query all
    events (excluding None).

    :type eventtype: str, list, tuple, or None

    :return: List of dictionary of the events.

    :rtype: list
    """
    with session_scope(engine) as session:
        queryset = session.query(table).filter(
            table.eventdate >= starttime,
            table.eventdate < endtime,
        )
        if isinstance(eventtype, str):
            queryset = queryset.filter(table.eventtype == eventtype)
        elif isinstance(eventtype, (list, tuple)):
            queryset = queryset.filter(table.eventtype.in_(eventtype))
        else:
            queryset = queryset.filter(table.eventtype != None)

        results = queryset.order_by(table.eventdate).all()
        return [object_as_dict(item) for item in results]


def get_bulletin_modified_by_range(engine, table, starttime, endtime,
                                   eventtype=None):
    """
    Get bulletin (only modified events) by particular time range and eventtype.
    If eventtype is None, query all events.

    :param engine: SQLAlchemy engine.

    :type engine: :class:`sqlalchemy.engine.base.Engine`

    :param table: SQLAlchemy model or table.

    :param starttime: Start time of the query.

    :type starttime: datetime.datetime

    :param endtime: End time of the query.

    :type endtime: datetime.datetime

    :param eventtype: Event type, e.g. VTA, VTB, MP. If you want to query
    multiple eventtypes, pass a list or tuple. If eventtype is None, query all
    events (excluding None).

    :type eventtype: str, list, tuple, or None

    :return: List of dictionary of the events.

    :rtype: list
    """
    with session_scope(engine) as session:
        queryset = session.query(table).filter(
            table.last_modified >= starttime,
            table.last_modified < endtime,
        )
        if isinstance(eventtype, str):
            queryset = queryset.filter(table.eventtype == eventtype)
        elif isinstance(eventtype, (list, tuple)):
            queryset = queryset.filter(table.eventtype.in_(eventtype))
        else:
            queryset = queryset.filter(table.eventtype != None)

        results = queryset.order_by(table.eventdate).all()
        return [object_as_dict(item) for item in results]


def get_bulletin_by_id(engine, table, eventid):
    """
    Get bulletin by its eventid. If not found, return None.

    param engine: SQLAlchemy engine.

    :type engine: :class:`sqlalchemy.engine.base.Engine`

    :param table: SQLAlchemy model or table.

    :param eventid: Event ID, e.g. 2021-07#3414.

    :type eventid: str

    :return: Dictionary of event if exists. Otherwise, return None.

    :rtype: dict or None
    """
    with session_scope(engine) as session:
        queryset = session.query(table).get(eventid)
        return object_as_dict(queryset) if queryset is not None else None

import json

from dateutil.parser import parse
from sqlalchemy import inspect


def load_config(path):
    """Load JSON config file."""
    with open(path, 'r') as fd:
        return json.load(fd)


def object_as_dict(obj):
    """Convert SQLAlchemy model to dictionary."""
    return {
        item.key: getattr(obj, item.key)
        for item in inspect(obj).mapper.column_attrs
    }


def is_valid_datetime(value):
    """Check if particular value string is valid datetime."""
    try:
        dateobj = parse(value)
        if dateobj is None:
            return False
        return True
    except Exception:
        return False


def parse_datetime_naive(value):
    """Parse value string to naive datetime, i.e. omitting time zone info."""
    dateobj = parse(value)
    if dateobj.tzinfo is not None:
        return dateobj.replace(tzinfo=None)
    return dateobj

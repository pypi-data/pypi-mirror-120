import argparse
import sys
import os

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from . import exceptions, query, settings, utils
from .models import Base, Bulletin
from .version import __version__


def parse_args():
    parser = argparse.ArgumentParser(
        description='Query seismic bulletin database (v{})'.format(__version__))

    parser.add_argument(
        '-s', '--start',
        help="Start time of query in 'YYYY-mm-dd HH:MM:SS' format. "
             "Time part is optional. By default start time is in Asia/Jakarta "
             "time zone.")

    parser.add_argument(
        '-e', '--end',
        help="End time of query in 'YYYY-mm-dd HH:MM:SS' format. "
             "Time part is optional. By default end time is in Asia/Jakarta "
             "time zone.")

    parser.add_argument(
        '-u', '--eventid',
        help="Event ID, e.g. 2021-07#2355.")

    parser.add_argument(
        '-t', '--eventtype',
        nargs='+',
        help='Event type to query, e.g. VTA, VTB, MP. If not provided, '
             'the script will query all event types. You can also add more '
             'than one event types.')

    parser.add_argument(
        '-o', '--output',
        help='Path to store query result to the CSV file. If not provided, '
             'the script will output the results to the standard output.')

    parser.add_argument(
        '-l', '--long-format',
        action='store_true',
        help='If provided, all bulletin fields will be printed.')

    parser.add_argument(
        '-d', '--delimiter',
        default=',',
        help='CSV delimiter. Default to comma (,).')

    parser.add_argument(
        '-c', '--config',
        default=settings.CONFIG_PATH,
        help='Path to the querybulletin JSON config file.')

    parser.add_argument(
        '-m', '--modified',
        action='store_true',
        help='If provided, query events in the bulletin that was modified '
        'since start and before end time.')

    return parser.parse_args()


def validate_args(args):
    if args.start:
        if not utils.is_valid_datetime(args.start):
            raise ValueError(
                "Start time value '{}' is not a valid datetime."
                "".format(args.start))

    if args.end:
        if not utils.is_valid_datetime(args.end):
            raise ValueError(
                "End time value '{}' is not a valid datetime."
                "".format(args.end))

    if not os.path.isfile(args.config):
        raise exceptions.ImproperlyConfigured(
            "JSON config file for querybulletin is not found. ")


def main():
    args = parse_args()
    validate_args(args)

    config = utils.load_config(args.config)
    engine_url = config.get('dburl')
    if engine_url is None:
        raise exceptions.ImproperlyConfigured(
            'dburl field in the config.json is not set.')

    engine = create_engine(engine_url, poolclass=NullPool)
    Base.prepare(engine, reflect=True)
    eventtype = args.eventtype
    events = []

    if args.start and args.end:
        start = utils.parse_datetime_naive(args.start)
        end = utils.parse_datetime_naive(args.end)
        if args.modified:
            events = query.get_bulletin_modified_by_range(
                engine,
                Bulletin,
                start,
                end,
                eventtype=eventtype,
            )
        else:
            events = query.get_bulletin_by_range(
                engine,
                Bulletin,
                start,
                end,
                eventtype=eventtype,
            )

    if args.eventid:
        event = query.get_bulletin_by_id(engine, Bulletin, args.eventid)
        if event is not None:
            events = [event, ]
        else:
            events = []

    if events:
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        df = pd.DataFrame(events)
        if args.output:
            if args.output.lower() == 'stdout':
                output = sys.stdout
            else:
                output = args.output

            if args.long_format:
                df.to_csv(output,
                          index=False,
                          sep=args.delimiter)
            else:
                df[settings.DEFAULT_COLUMNS].to_csv(output,
                                                    index=False,
                                                    sep=args.delimiter)
        else:
            if args.long_format:
                print(df, file=sys.stdout)
            else:
                print(df[settings.DEFAULT_COLUMNS], file=sys.stdout)
    else:
        # Empty events.
        df = pd.DataFrame()
        if args.output:
            if args.output.lower() == 'stdout':
                output = sys.stdout
            else:
                output = args.output

            df.to_csv(output, index=False, sep=args.delimiter)

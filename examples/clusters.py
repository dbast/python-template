#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Helper to manage AWS EMR clusters

There must be either the right credentials via the standard AWS machanism (env
variables or something in ~.aws) or the machine, where this is executed, has a
required AWS IAM role.
"""

import logging
import datetime
import json
import os
import sys
import boto3

DEFAULT_REGION = "eu-west-1"

logger = logging.getLogger()  # pylint: disable=locally-disabled, invalid-name
logger.setLevel(logging.INFO)


def _list_clusters(client, days=60):
    """List running Clusters"""
    response = client.list_clusters(
        CreatedAfter=datetime.datetime.now() - datetime.timedelta(days=days),
        ClusterStates=['STARTING', 'BOOTSTRAPPING', 'RUNNING', 'WAITING'],
    )
    logger.info('Current active clusters: "%s"', json.dumps(response, indent=4, sort_keys=True))
    return True


def lambda_list_handler(event, context):  # pylint: disable=locally-disabled, unused-argument
    """Lambda list-event-handler"""
    logger.info('Starting to process the list event')
    region = os.getenv('CLUSTERS_REGION', DEFAULT_REGION)

    client = boto3.client('emr', region_name=region)
    success = _list_clusters(client)
    if not success:
        raise Exception('Listing failed.')

    logger.info('Successfully listed clusters')


def _cli_list(args):
    """List helper for the cli"""
    client = boto3.client('emr', region_name=args.region)
    return _list_clusters(client, args.days)


def cli():
    """cli entrypoint for local execution"""
    import argparse  # Import here, the lambda handler does not need this
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Manage running clusters')
    parser.add_argument('-r', '--region', default=DEFAULT_REGION,
                        help='The aws region to be used (default: %(default)s)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Increase log verbosity')
    subparsers = parser.add_subparsers()
    parser_list = subparsers.add_parser('list')
    parser_list.set_defaults(func=_cli_list)
    parser_list.add_argument(
        '--days', type=int, default=60,
        help='Only list active clusters created in the last given days (default: %(default)s)')

    args = parser.parse_args()
    logger.info('Got the following cli arguments: "%s"', args)

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    success = args.func(args)
    if not success:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(cli())

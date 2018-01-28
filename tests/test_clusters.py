# pylint: skip-file

import pytest
from mock import patch, Mock, call

from examples.clusters import (
    DEFAULT_REGION, _list_clusters, lambda_list_handler
    )


@pytest.mark.parametrize("test_input,expected_value", [
    ([], True),
    ([{'Id': 'id1', 'Name': 'Name1'}, {'Id': 'id2', 'Name': 'Name2'}], True),
])
def test__list_cluster__clusters_running_mode__return_value(test_input, expected_value):
    test_client = Mock()
    test_client.list_clusters.return_value = {'Clusters': test_input}

    assert _list_clusters(test_client) == expected_value


@patch("examples.clusters._list_clusters")
@patch("examples.clusters.boto3")
@patch("examples.clusters.os")
def test_lambda_list_handler__running_clusters__list_successful(patched_os,
                                                                patched_boto,
                                                                patched_list_clusters):
    test_region = '123'
    patched_os.getenv.return_value = test_region

    lambda_list_handler({}, {})

    patched_list_clusters.assert_called_once_with(patched_boto.client())
    patched_boto.client.assert_has_calls([call('emr', region_name=test_region), call()])
    patched_os.getenv.assert_called_once_with('CLUSTERS_REGION', DEFAULT_REGION)


@patch("examples.clusters._list_clusters")
@patch("examples.clusters.boto3")
def test_lambda_list_handler__list_not_successful__exception_raised(patched_boto,
                                                                    patched_list_clusters):
    patched_list_clusters.return_value = False

    with pytest.raises(Exception):
        lambda_list_handler({}, {})

    patched_list_clusters.assert_called_once_with(patched_boto.client())

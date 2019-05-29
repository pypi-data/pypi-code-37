import os

import pytest
from algernon.aws.gql import GqlNotary


@pytest.mark.gql_i
class TestGql:
    def test_gql_query(self):
        os.environ['DEBUG'] = 'False'
        query = '''query RetrieveHistory($flow_run_id: String!, $token: String){ listStateEntries(filter: {flow_run_id: {eq: $flow_run_id}}, nextToken: $token){ items{ flow_run_id state_id state_type state_timestamp state_properties{property_name property_value}}nextToken}}'''
        variables = {'flow_run_id': 'test_flow#1001'}
        gql_endpoint = 'w7ppoindq5hrvpx3tpseisrku4.appsync-api.us-east-1.amazonaws.com'
        notary = GqlNotary(gql_endpoint)
        results = notary.send(query, variables)
        assert results
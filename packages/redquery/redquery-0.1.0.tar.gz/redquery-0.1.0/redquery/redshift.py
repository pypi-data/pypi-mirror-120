import logging
import time
from dataclasses import dataclass
from functools import cached_property
from typing import List, Optional

import boto3
from botocore.config import Config
from mypy_boto3_redshift_data import Client as RedshiftDataAPI
from mypy_boto3_redshift_data.paginator import GetStatementResultPaginator
from mypy_boto3_redshift_data.type_defs import (
    DescribeStatementResponseTypeDef, GetStatementResultResponseTypeDef)

from redquery.errors import ActiveStatementsLimitExceeded, RedshiftError
from redquery.formatting import Row, format_as_dict

logger = logging.getLogger(__name__)


@dataclass
class Redshift:
    """Redshift Data API interface."""

    cluster_identifier: str
    database_name: str
    database_user: str

    @cached_property
    def client(self) -> RedshiftDataAPI:
        """Construct Redshift Data API client."""
        config = Config(
            retries={
                'max_attempts': 10,
                'mode': 'standard',
            },
        )
        return boto3.client('redshift-data', config=config)

    def submit(
        self,
        query: str,
        query_name: Optional[str] = None,
        notify_event_bridge: bool = False,
    ) -> str:
        """Submit SQL query and get back its identifier."""
        # StatementName must only be provided if it is non empty, otherwise we
        # will get a ParamValidationError.
        extra_args = {
            'StatementName': query_name,
        } if query_name else {}

        try:
            return self.client.execute_statement(
                ClusterIdentifier=self.cluster_identifier,
                Database=self.database_name,
                DbUser=self.database_user,

                Sql=query,
                WithEvent=notify_event_bridge,

                **extra_args,
            )['Id']
        except self.client.exceptions.ExecuteStatementException as err:
            raise ActiveStatementsLimitExceeded() from err

    def describe(self, query_id: str) -> DescribeStatementResponseTypeDef:
        """Get statement status."""
        statement = self.client.describe_statement(Id=query_id)

        if error_description := statement.get('Error'):
            raise RedshiftError(description=error_description)

        return statement

    def retrieve(
        self,
        query_id: str,
    ) -> Optional[List[GetStatementResultResponseTypeDef]]:
        """Get query result by id."""
        paginator: GetStatementResultPaginator = self.client.get_paginator(
            'get_statement_result',
        )
        response_iterator = paginator.paginate(Id=query_id)

        try:
            return list(response_iterator)
        except self.client.exceptions.ResourceNotFoundException:
            # Not every query returns results. Nothing is returned if, say, we
            # executed a CREATE TABLE statement.
            return None

    def is_complete(self, query_id: str) -> bool:
        """Determine if given SQL query is complete."""
        description = self.describe(query_id=query_id)
        return description['Status'] == 'FINISHED'

    def execute(
        self,
        query: str,
        query_name: Optional[str] = None,
        notify_event_bridge: bool = False,
        timeout: int = 3,
    ) -> List[Row]:
        """Submit SQL query and get back its result."""
        query_id = self.submit(
            query=query,
            query_name=query_name,
            notify_event_bridge=notify_event_bridge,
        )

        while not self.is_complete(query_id):
            time.sleep(timeout)

        return list(format_as_dict(self.retrieve(query_id)))

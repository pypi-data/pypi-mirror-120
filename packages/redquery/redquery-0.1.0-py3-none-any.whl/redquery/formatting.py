from typing import List, Optional

from more_itertools import first
from mypy_boto3_redshift_data.type_defs import (
    GetStatementResultResponseTypeDef,
)

from redquery.models import Row


def format_as_dict(
    response: Optional[List[GetStatementResultResponseTypeDef]],
) -> Optional[List[Row]]:
    """Format Response query result as a list of dicts."""
    try:
        first_row = first(response)
    except ValueError:
        return None

    column_labels = [
        column['label']
        for column in first_row['ColumnMetadata']
    ]

    for row in response:
        for sub_row in row['Records']:
            values = [
                first(cell.values())
                for cell in sub_row
            ]

            yield dict(zip(column_labels, values))

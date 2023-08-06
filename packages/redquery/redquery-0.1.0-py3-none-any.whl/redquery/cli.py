import json

from typer import Context, Option, Typer, echo

from redquery.formatting import format_as_dict
from redquery.redshift import Redshift

app = Typer()


class RedshiftContext(Context):
    """Signify that we write a Redshift instance into ctx.obj."""
    obj: Redshift


@app.callback()
def configure(
    ctx: RedshiftContext,
    cluster: str = Option(
        ...,
        envvar='REDQUERY_CLUSTER_NAME',
        help='Redshift cluster identifier',
    ),
    db: str = Option(
        ...,
        envvar='REDQUERY_DB',
        help='Database name',
    ),
    user: str = Option(
        ...,
        envvar='REDQUERY_DB_USER',
        help='Database user name'
    ),
):
    """Run SQL queries against AWS Redshift using HTTP Data API."""
    ctx.obj = Redshift(
        cluster_identifier=cluster,
        database_name=db,
        database_user=user,
    )


@app.command()
def query(ctx: RedshiftContext, sql: str):
    """Run an SQL query, wait for result, and print it."""
    echo(
        json.dumps(
            ctx.obj.execute(sql),
            indent=2,
        ),
    )


@app.command()
def submit(ctx: RedshiftContext, sql: str):
    """Submit an SQL statement to the server and return statement ID."""
    echo(ctx.obj.submit(sql))


@app.command()
def retrieve(ctx: RedshiftContext, statement_id: str):
    """Retrieve result of the specified statement by ID."""
    echo(list(format_as_dict(ctx.obj.retrieve(statement_id))))

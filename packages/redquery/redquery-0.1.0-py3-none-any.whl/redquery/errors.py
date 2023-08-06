from dataclasses import dataclass

from documented import DocumentedError


@dataclass
class RedshiftError(DocumentedError):
    """AWS Redshift failed to execute query. {self.description}."""

    description: str


@dataclass
class ActiveStatementsLimitExceeded(DocumentedError):
    """Limit of simultaneously running Data API queries exceeded."""

"""
Provide forms for command line interface's transaction commands.
"""
from marshmallow import (
    Schema,
    fields,
    validate,
)

from cli.generic.forms.fields import (
    FamilyNameField,
    NodeUrlField,
    TransactionIdentifierField,
    TransactionIdentifiersListField,
)


class GetTransactionsListForm(Schema):
    """
    Get a list of transactions form.
    """

    ids = TransactionIdentifiersListField(allow_none=True, required=False)
    start = TransactionIdentifierField(allow_none=True, required=False)
    head = TransactionIdentifierField(allow_none=True, required=False)
    limit = fields.Integer(
        allow_none=True,
        strict=True,
        required=False,
        validate=[
            validate.Range(min=1, error='Limit must be greater than 0.'),
        ],
    )
    family_name = FamilyNameField(allow_none=True, required=False)
    node_url = NodeUrlField(required=False)


class GetTransactionForm(Schema):
    """
    Get transaction form.
    """

    id = TransactionIdentifierField(allow_none=True, required=True)
    node_url = NodeUrlField(required=False)

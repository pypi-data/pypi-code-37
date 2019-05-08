# DO NOT EDIT! This file is automatically generated

import marshmallow
import marshmallow_enum

from commercetools import types

__all__ = [
    "MyCartDraftSchema",
    "MyCustomerDraftSchema",
    "MyLineItemDraftSchema",
    "MyOrderFromCartDraftSchema",
]


class MyCartDraftSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.MyCartDraft`."
    currency = marshmallow.fields.String()
    customer_email = marshmallow.fields.String(
        allow_none=True, missing=None, data_key="customerEmail"
    )
    country = marshmallow.fields.String(allow_none=True, missing=None)
    inventory_mode = marshmallow_enum.EnumField(
        types.InventoryMode, by_value=True, missing=None, data_key="inventoryMode"
    )
    line_items = marshmallow.fields.Nested(
        nested="commercetools.schemas._me.MyLineItemDraftSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        many=True,
        missing=None,
        data_key="lineItems",
    )
    shipping_address = marshmallow.fields.Nested(
        nested="commercetools.schemas._common.AddressSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        missing=None,
        data_key="shippingAddress",
    )
    billing_address = marshmallow.fields.Nested(
        nested="commercetools.schemas._common.AddressSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        missing=None,
        data_key="billingAddress",
    )
    shipping_method = marshmallow.fields.Nested(
        nested="commercetools.schemas._shipping_method.ShippingMethodReferenceSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        missing=None,
        data_key="shippingMethod",
    )
    custom = marshmallow.fields.Nested(
        nested="commercetools.schemas._type.CustomFieldsDraftSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        missing=None,
    )
    locale = marshmallow.fields.String(allow_none=True, missing=None)
    tax_mode = marshmallow_enum.EnumField(
        types.TaxMode, by_value=True, missing=None, data_key="taxMode"
    )
    delete_days_after_last_modification = marshmallow.fields.Integer(
        allow_none=True, missing=None, data_key="deleteDaysAfterLastModification"
    )
    item_shipping_addresses = marshmallow.fields.Nested(
        nested="commercetools.schemas._common.AddressSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        many=True,
        missing=None,
        data_key="itemShippingAddresses",
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.MyCartDraft(**data)


class MyCustomerDraftSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.MyCustomerDraft`."
    email = marshmallow.fields.String(allow_none=True)
    password = marshmallow.fields.String(allow_none=True)
    first_name = marshmallow.fields.String(
        allow_none=True, missing=None, data_key="firstName"
    )
    last_name = marshmallow.fields.String(
        allow_none=True, missing=None, data_key="lastName"
    )
    middle_name = marshmallow.fields.String(
        allow_none=True, missing=None, data_key="middleName"
    )
    title = marshmallow.fields.String(allow_none=True, missing=None)
    date_of_birth = marshmallow.fields.Date(
        allow_none=True, missing=None, data_key="dateOfBirth"
    )
    company_name = marshmallow.fields.String(
        allow_none=True, missing=None, data_key="companyName"
    )
    vat_id = marshmallow.fields.String(allow_none=True, missing=None, data_key="vatId")
    addresses = marshmallow.fields.Nested(
        nested="commercetools.schemas._common.AddressSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        many=True,
        missing=None,
    )
    default_shipping_address = marshmallow.fields.Integer(
        allow_none=True, missing=None, data_key="defaultShippingAddress"
    )
    default_billing_address = marshmallow.fields.Integer(
        allow_none=True, missing=None, data_key="defaultBillingAddress"
    )
    custom = marshmallow.fields.Nested(
        nested="commercetools.schemas._type.CustomFieldsSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        missing=None,
    )
    locale = marshmallow.fields.String(allow_none=True, missing=None)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.MyCustomerDraft(**data)


class MyLineItemDraftSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.MyLineItemDraft`."
    product_id = marshmallow.fields.String(allow_none=True, data_key="productId")
    variant_id = marshmallow.fields.Integer(allow_none=True, data_key="variantId")
    quantity = marshmallow.fields.Integer(allow_none=True)
    supply_channel = marshmallow.fields.Nested(
        nested="commercetools.schemas._channel.ChannelReferenceSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        missing=None,
        data_key="supplyChannel",
    )
    distribution_channel = marshmallow.fields.Nested(
        nested="commercetools.schemas._channel.ChannelReferenceSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        missing=None,
        data_key="distributionChannel",
    )
    custom = marshmallow.fields.Nested(
        nested="commercetools.schemas._type.CustomFieldsDraftSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        missing=None,
    )
    shipping_details = marshmallow.fields.Nested(
        nested="commercetools.schemas._cart.ItemShippingDetailsDraftSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        missing=None,
        data_key="shippingDetails",
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.MyLineItemDraft(**data)


class MyOrderFromCartDraftSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.MyOrderFromCartDraft`."
    id = marshmallow.fields.String(allow_none=True)
    version = marshmallow.fields.Integer(allow_none=True)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.MyOrderFromCartDraft(**data)

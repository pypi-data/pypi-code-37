# DO NOT EDIT! This file is automatically generated

import marshmallow
import marshmallow_enum

from commercetools import helpers, types
from commercetools.schemas._base import (
    PagedQueryResponseSchema,
    UpdateActionSchema,
    UpdateSchema,
)
from commercetools.schemas._common import (
    LocalizedStringField,
    ReferenceSchema,
    ResourceSchema,
)

__all__ = [
    "CustomFieldBooleanTypeSchema",
    "CustomFieldDateTimeTypeSchema",
    "CustomFieldDateTypeSchema",
    "CustomFieldEnumTypeSchema",
    "CustomFieldEnumValueSchema",
    "CustomFieldLocalizedEnumTypeSchema",
    "CustomFieldLocalizedEnumValueSchema",
    "CustomFieldLocalizedStringTypeSchema",
    "CustomFieldMoneyTypeSchema",
    "CustomFieldNumberTypeSchema",
    "CustomFieldReferenceTypeSchema",
    "CustomFieldSetTypeSchema",
    "CustomFieldStringTypeSchema",
    "CustomFieldTimeTypeSchema",
    "CustomFieldsDraftSchema",
    "CustomFieldsSchema",
    "FieldDefinitionSchema",
    "FieldTypeSchema",
    "TypeAddEnumValueActionSchema",
    "TypeAddFieldDefinitionActionSchema",
    "TypeAddLocalizedEnumValueActionSchema",
    "TypeChangeEnumValueOrderActionSchema",
    "TypeChangeFieldDefinitionLabelActionSchema",
    "TypeChangeFieldDefinitionOrderActionSchema",
    "TypeChangeKeyActionSchema",
    "TypeChangeLabelActionSchema",
    "TypeChangeLocalizedEnumValueOrderActionSchema",
    "TypeChangeNameActionSchema",
    "TypeDraftSchema",
    "TypePagedQueryResponseSchema",
    "TypeReferenceSchema",
    "TypeRemoveFieldDefinitionActionSchema",
    "TypeSchema",
    "TypeSetDescriptionActionSchema",
    "TypeUpdateActionSchema",
    "TypeUpdateSchema",
]


class FieldContainerField(marshmallow.fields.Dict):
    def _deserialize(self, value, attr, data):
        result = super()._deserialize(value, attr, data)
        return types.FieldContainer(**result)


class CustomFieldEnumValueSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.CustomFieldEnumValue`."
    key = marshmallow.fields.String(allow_none=True)
    label = marshmallow.fields.String(allow_none=True)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.CustomFieldEnumValue(**data)


class CustomFieldLocalizedEnumValueSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.CustomFieldLocalizedEnumValue`."
    key = marshmallow.fields.String(allow_none=True)
    label = LocalizedStringField(allow_none=True)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.CustomFieldLocalizedEnumValue(**data)


class CustomFieldsDraftSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.CustomFieldsDraft`."
    type = marshmallow.fields.Nested(
        nested="commercetools.schemas._common.ResourceIdentifierSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
    )
    fields = FieldContainerField(allow_none=True, missing=None)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.CustomFieldsDraft(**data)


class CustomFieldsSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.CustomFields`."
    type = marshmallow.fields.Nested(
        nested="commercetools.schemas._type.TypeReferenceSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
    )
    fields = FieldContainerField(allow_none=True)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.CustomFields(**data)


class FieldDefinitionSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.FieldDefinition`."
    type = marshmallow.fields.Dict(allow_none=True)
    name = marshmallow.fields.String(allow_none=True)
    label = LocalizedStringField(allow_none=True)
    required = marshmallow.fields.Bool(allow_none=True)
    input_hint = marshmallow_enum.EnumField(
        types.TypeTextInputHint, by_value=True, missing=None, data_key="inputHint"
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.FieldDefinition(**data)


class FieldTypeSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.FieldType`."
    name = marshmallow.fields.String(allow_none=True)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["name"]
        return types.FieldType(**data)


class TypeDraftSchema(marshmallow.Schema):
    "Marshmallow schema for :class:`commercetools.types.TypeDraft`."
    key = marshmallow.fields.String(allow_none=True)
    name = LocalizedStringField(allow_none=True)
    description = LocalizedStringField(allow_none=True, missing=None)
    resource_type_ids = marshmallow.fields.List(
        marshmallow_enum.EnumField(types.ResourceTypeId, by_value=True),
        data_key="resourceTypeIds",
    )
    field_definitions = marshmallow.fields.Nested(
        nested="commercetools.schemas._type.FieldDefinitionSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        many=True,
        missing=None,
        data_key="fieldDefinitions",
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.TypeDraft(**data)


class TypePagedQueryResponseSchema(PagedQueryResponseSchema):
    "Marshmallow schema for :class:`commercetools.types.TypePagedQueryResponse`."
    results = marshmallow.fields.Nested(
        nested="commercetools.schemas._type.TypeSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        many=True,
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.TypePagedQueryResponse(**data)


class TypeReferenceSchema(ReferenceSchema):
    "Marshmallow schema for :class:`commercetools.types.TypeReference`."
    obj = marshmallow.fields.Nested(
        nested="commercetools.schemas._type.TypeSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        missing=None,
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["type_id"]
        return types.TypeReference(**data)


class TypeSchema(ResourceSchema):
    "Marshmallow schema for :class:`commercetools.types.Type`."
    key = marshmallow.fields.String(allow_none=True)
    name = LocalizedStringField(allow_none=True)
    description = LocalizedStringField(allow_none=True, missing=None)
    resource_type_ids = marshmallow.fields.List(
        marshmallow_enum.EnumField(types.ResourceTypeId, by_value=True),
        data_key="resourceTypeIds",
    )
    field_definitions = marshmallow.fields.Nested(
        nested="commercetools.schemas._type.FieldDefinitionSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        many=True,
        data_key="fieldDefinitions",
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.Type(**data)


class TypeUpdateActionSchema(UpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.TypeUpdateAction`."

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.TypeUpdateAction(**data)


class TypeUpdateSchema(UpdateSchema):
    "Marshmallow schema for :class:`commercetools.types.TypeUpdate`."
    actions = marshmallow.fields.List(
        helpers.Discriminator(
            discriminator_field=("action", "action"),
            discriminator_schemas={
                "addEnumValue": "commercetools.schemas._type.TypeAddEnumValueActionSchema",
                "addFieldDefinition": "commercetools.schemas._type.TypeAddFieldDefinitionActionSchema",
                "addLocalizedEnumValue": "commercetools.schemas._type.TypeAddLocalizedEnumValueActionSchema",
                "changeEnumValueOrder": "commercetools.schemas._type.TypeChangeEnumValueOrderActionSchema",
                "changeFieldDefinitionLabel": "commercetools.schemas._type.TypeChangeFieldDefinitionLabelActionSchema",
                "changeFieldDefinitionOrder": "commercetools.schemas._type.TypeChangeFieldDefinitionOrderActionSchema",
                "changeKey": "commercetools.schemas._type.TypeChangeKeyActionSchema",
                "changeLabel": "commercetools.schemas._type.TypeChangeLabelActionSchema",
                "changeLocalizedEnumValueOrder": "commercetools.schemas._type.TypeChangeLocalizedEnumValueOrderActionSchema",
                "changeName": "commercetools.schemas._type.TypeChangeNameActionSchema",
                "removeFieldDefinition": "commercetools.schemas._type.TypeRemoveFieldDefinitionActionSchema",
                "setDescription": "commercetools.schemas._type.TypeSetDescriptionActionSchema",
            },
            unknown=marshmallow.EXCLUDE,
            allow_none=True,
        ),
        allow_none=True,
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        return types.TypeUpdate(**data)


class CustomFieldBooleanTypeSchema(FieldTypeSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomFieldBooleanType`."

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["name"]
        return types.CustomFieldBooleanType(**data)


class CustomFieldDateTimeTypeSchema(FieldTypeSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomFieldDateTimeType`."

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["name"]
        return types.CustomFieldDateTimeType(**data)


class CustomFieldDateTypeSchema(FieldTypeSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomFieldDateType`."

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["name"]
        return types.CustomFieldDateType(**data)


class CustomFieldEnumTypeSchema(FieldTypeSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomFieldEnumType`."
    values = marshmallow.fields.Nested(
        nested="commercetools.schemas._type.CustomFieldEnumValueSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        many=True,
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["name"]
        return types.CustomFieldEnumType(**data)


class CustomFieldLocalizedEnumTypeSchema(FieldTypeSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomFieldLocalizedEnumType`."
    values = marshmallow.fields.Nested(
        nested="commercetools.schemas._type.CustomFieldLocalizedEnumValueSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        many=True,
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["name"]
        return types.CustomFieldLocalizedEnumType(**data)


class CustomFieldLocalizedStringTypeSchema(FieldTypeSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomFieldLocalizedStringType`."

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["name"]
        return types.CustomFieldLocalizedStringType(**data)


class CustomFieldMoneyTypeSchema(FieldTypeSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomFieldMoneyType`."

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["name"]
        return types.CustomFieldMoneyType(**data)


class CustomFieldNumberTypeSchema(FieldTypeSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomFieldNumberType`."

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["name"]
        return types.CustomFieldNumberType(**data)


class CustomFieldReferenceTypeSchema(FieldTypeSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomFieldReferenceType`."
    reference_type_id = marshmallow_enum.EnumField(
        types.ReferenceTypeId, by_value=True, data_key="referenceTypeId"
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["name"]
        return types.CustomFieldReferenceType(**data)


class CustomFieldSetTypeSchema(FieldTypeSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomFieldSetType`."
    element_type = helpers.Discriminator(
        discriminator_field=("name", "name"),
        discriminator_schemas={
            "Boolean": "commercetools.schemas._type.CustomFieldBooleanTypeSchema",
            "DateTime": "commercetools.schemas._type.CustomFieldDateTimeTypeSchema",
            "Date": "commercetools.schemas._type.CustomFieldDateTypeSchema",
            "Enum": "commercetools.schemas._type.CustomFieldEnumTypeSchema",
            "LocalizedEnum": "commercetools.schemas._type.CustomFieldLocalizedEnumTypeSchema",
            "LocalizedString": "commercetools.schemas._type.CustomFieldLocalizedStringTypeSchema",
            "Money": "commercetools.schemas._type.CustomFieldMoneyTypeSchema",
            "Number": "commercetools.schemas._type.CustomFieldNumberTypeSchema",
            "Reference": "commercetools.schemas._type.CustomFieldReferenceTypeSchema",
            "Set": "commercetools.schemas._type.CustomFieldSetTypeSchema",
            "String": "commercetools.schemas._type.CustomFieldStringTypeSchema",
            "Time": "commercetools.schemas._type.CustomFieldTimeTypeSchema",
        },
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        data_key="elementType",
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["name"]
        return types.CustomFieldSetType(**data)


class CustomFieldStringTypeSchema(FieldTypeSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomFieldStringType`."

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["name"]
        return types.CustomFieldStringType(**data)


class CustomFieldTimeTypeSchema(FieldTypeSchema):
    "Marshmallow schema for :class:`commercetools.types.CustomFieldTimeType`."

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["name"]
        return types.CustomFieldTimeType(**data)


class TypeAddEnumValueActionSchema(TypeUpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.TypeAddEnumValueAction`."
    field_name = marshmallow.fields.String(allow_none=True, data_key="fieldName")
    value = marshmallow.fields.Nested(
        nested="commercetools.schemas._type.CustomFieldEnumValueSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.TypeAddEnumValueAction(**data)


class TypeAddFieldDefinitionActionSchema(TypeUpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.TypeAddFieldDefinitionAction`."
    field_definition = marshmallow.fields.Nested(
        nested="commercetools.schemas._type.FieldDefinitionSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
        data_key="fieldDefinition",
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.TypeAddFieldDefinitionAction(**data)


class TypeAddLocalizedEnumValueActionSchema(TypeUpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.TypeAddLocalizedEnumValueAction`."
    field_name = marshmallow.fields.String(allow_none=True, data_key="fieldName")
    value = marshmallow.fields.Nested(
        nested="commercetools.schemas._type.CustomFieldLocalizedEnumValueSchema",
        unknown=marshmallow.EXCLUDE,
        allow_none=True,
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.TypeAddLocalizedEnumValueAction(**data)


class TypeChangeEnumValueOrderActionSchema(TypeUpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.TypeChangeEnumValueOrderAction`."
    field_name = marshmallow.fields.String(allow_none=True, data_key="fieldName")
    keys = marshmallow.fields.List(marshmallow.fields.String(allow_none=True))

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.TypeChangeEnumValueOrderAction(**data)


class TypeChangeFieldDefinitionLabelActionSchema(TypeUpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.TypeChangeFieldDefinitionLabelAction`."
    field_name = marshmallow.fields.String(allow_none=True, data_key="fieldName")
    label = LocalizedStringField(allow_none=True)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.TypeChangeFieldDefinitionLabelAction(**data)


class TypeChangeFieldDefinitionOrderActionSchema(TypeUpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.TypeChangeFieldDefinitionOrderAction`."
    field_names = marshmallow.fields.List(
        marshmallow.fields.String(allow_none=True), data_key="fieldNames"
    )

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.TypeChangeFieldDefinitionOrderAction(**data)


class TypeChangeKeyActionSchema(TypeUpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.TypeChangeKeyAction`."
    key = marshmallow.fields.String(allow_none=True)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.TypeChangeKeyAction(**data)


class TypeChangeLabelActionSchema(TypeUpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.TypeChangeLabelAction`."
    field_name = marshmallow.fields.String(allow_none=True, data_key="fieldName")
    label = LocalizedStringField(allow_none=True)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.TypeChangeLabelAction(**data)


class TypeChangeLocalizedEnumValueOrderActionSchema(TypeUpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.TypeChangeLocalizedEnumValueOrderAction`."
    field_name = marshmallow.fields.String(allow_none=True, data_key="fieldName")
    keys = marshmallow.fields.List(marshmallow.fields.String(allow_none=True))

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.TypeChangeLocalizedEnumValueOrderAction(**data)


class TypeChangeNameActionSchema(TypeUpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.TypeChangeNameAction`."
    name = LocalizedStringField(allow_none=True)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.TypeChangeNameAction(**data)


class TypeRemoveFieldDefinitionActionSchema(TypeUpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.TypeRemoveFieldDefinitionAction`."
    field_name = marshmallow.fields.String(allow_none=True, data_key="fieldName")

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.TypeRemoveFieldDefinitionAction(**data)


class TypeSetDescriptionActionSchema(TypeUpdateActionSchema):
    "Marshmallow schema for :class:`commercetools.types.TypeSetDescriptionAction`."
    description = LocalizedStringField(allow_none=True, missing=None)

    class Meta:
        unknown = marshmallow.EXCLUDE

    @marshmallow.post_load
    def post_load(self, data):
        del data["action"]
        return types.TypeSetDescriptionAction(**data)

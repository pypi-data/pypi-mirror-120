from importlib import import_module
from logging import getLogger
from random import shuffle
from typing import Any, Dict, List, Tuple, Type
from uuid import uuid4

from OpenApiDriver.dto_base import Dto, ResourceRelation, IdDependency, IdReference

logger = getLogger(__name__)


class DtoMixin:
    def get_invalidated_data(
            self, schema: Dict[str, Any], status_code: int
        ) -> Dict[str, Any]:
        properties: Dict[str, Any] = self.__dict__

        dependencies: List[ResourceRelation] = self.get_dependencies()
        shuffle(dependencies)
        for dependency in dependencies:
            if isinstance(dependency, IdDependency) and status_code == dependency.error_code:
                invalid_value = uuid4().hex
                logger.debug(
                    f"Breaking IdDependency for status_code {status_code}: replacing "
                    f"{properties[dependency.property_name]} with {invalid_value}"
                )
                properties[dependency.property_name] = invalid_value
                return properties

        constrained_properties: List[ResourceRelation] = [
            c.property_name for c in self.get_constraints()
        ]
        property_names = list(properties.keys())
        # shuffle the propery_names so different properties on the Dto are invalidated
        # when rerunning the test
        shuffle(property_names)
        for property_name in property_names:
            # if possible, invalidate a constraint but send otherwise valid data
            property_data = schema["properties"][property_name]
            property_type = property_data["type"]
            current_value = properties[property_name]
            if enum_values := property_data.get("enum"):
                invalidated_value = self.get_invalid_value_from_enum(
                    values=enum_values, value_type=property_type
                )
                if invalidated_value is not None:
                    properties[property_name] = invalidated_value
                    return properties
            if property_type == "boolean" and property_name in constrained_properties:
                properties[property_name] = not current_value
                return properties
            if property_type == "integer":
                if minimum := property_data.get("minimum"):
                    properties[property_name] = minimum - 1
                    return properties
                if maximum := property_data.get("maximum"):
                    properties[property_name] = maximum + 1
                    return properties
                if property_name in constrained_properties:
                    #TODO: figure out a good generic approach, also consider multiple
                    # constraints on the same property
                    #HACK: this int is way out of the json supported int range
                    properties[property_name] = uuid4().int
                    return properties
            if property_type == "number":
                if minimum := property_data.get("minimum"):
                    properties[property_name] = minimum - 1
                    return properties
                if maximum := property_data.get("maximum"):
                    properties[property_name] = maximum + 1
                    return properties
                if property_name in constrained_properties:
                    #TODO: figure out a good generic approach, also consider multiple
                    # constraints on the same property
                    #HACK: this float is way out of the json supported float range
                    properties[property_name] = uuid4().int / 3.14
                    return properties
            if property_type == "string":
                if minimum := property_data.get("minLength"):
                    if minimum > 0:
                        # if there is a minimum length, send 1 character less
                        properties[property_name] = current_value[0:minimum-1]
                        return properties
                if maximum := property_data.get("maxLength"):
                    properties[property_name] = current_value + uuid4().hex
                    return properties
        # if there are no constraints to violate, send invalid data types
        schema_properties = schema["properties"]
        for property_name, property_values in schema_properties.items():
            property_type = property_values.get("type")
            if property_type != "string":
                logger.debug(
                    f"property {property_name} set to str instead of {property_type}"
                )
                properties[property_name] = uuid4().hex
            else:
                # Since int / float / bool can always be cast to sting,
                # change the string to a nested object
                properties[property_name] = [
                    {
                        "invalid": [
                            None
                        ]
                    }
                ]
        return properties

    @staticmethod
    def get_invalid_value_from_enum(values: List[Any], value_type: str):
        if value_type == "string":
            invalid_value: Any = ""
        elif value_type in ["integer", "number"]:
            invalid_value = 0
        elif value_type == "array":
            invalid_value = []
        elif value_type == "object":
            invalid_value = {}
        else:
            logger.warning(f"Cannot invalidate enum value with type {value_type}")
            return None
        for value in values:
            if value_type in ["string", "integer", "number"]:
                invalid_value += value
            #TODO: can the values to choose from in an enum be array/object in JSON?
            if value_type == "array":
                invalid_value.extend(value)
            if value_type == "object":
                invalid_value.update(value)
        return invalid_value


class ExtendedDto(Dto, DtoMixin):
    pass


def add_dto_mixin(dto: Dto) -> ExtendedDto:
    """Add the DtoMixin to a Dto class instance"""
    base_cls = dto.__class__
    base_cls_name = dto.__class__.__name__
    dto.__class__ = type(base_cls_name, (base_cls, DtoMixin),{})
    return dto


class get_dto_class:
    def __init__(self, mappings_module_name: str) -> None:
        try:
            mappings_module = import_module(mappings_module_name)
            self.dto_mapping: Dict[Tuple[str, str], Any] = mappings_module.DTO_MAPPING
        except (ImportError, AttributeError, ValueError) as exception:
            logger.debug(f"DTO_MAPPING was not imported: {exception}")
            self.dto_mapping = {}

    def __call__(self, endpoint: str, method: str) -> Type[Dto]:
        try:
            return self.dto_mapping[(endpoint, method)]
        except KeyError:
            logger.debug(f"No Dto mapping for {endpoint} {method}.")
            return Dto

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="ignore", # ignore extra attributes during model initialization
        validate_assignment=True,
        arbitrary_types_allowed=True, # allow user types for fields
        from_attributes=True,
        allow_inf_nan=False, # forbid infinity (`+inf` an `-inf`) and NaN values to float and decimal fields
        revalidate_instances="always", # revalidate models and dataclasses during validation
        ser_json_timedelta="float", # serialize timedeltas to the total number of seconds
        ser_json_bytes="base64",  # serialize bytes to URL safe base64 strings
        val_json_bytes="base64", # deserialize URL safe base64 strings to bytes
        validate_default=True,
        validate_return=True,
        coerce_numbers_to_str=True, # convert numbers to strings: 123 -> "123"
        regex_engine="python-re",
        use_attribute_docstrings=True,
        cache_strings="all",
        alias_generator=to_camel,
        populate_by_name=True
    )

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="allow",
        populate_by_name=True,
        use_enum_values=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        from_attributes=True,
        allow_inf_nan=False,
        revalidate_instances="always",
        ser_json_timedelta="float",
        ser_json_bytes="base64",
        val_json_bytes="base64",
        validate_default=True,
        validate_return=True,
        coerce_numbers_to_str=True,
        regex_engine="python-re",
        use_attribute_docstrings=True,
        cache_strings="all",
        alias_generator=to_camel,
    )

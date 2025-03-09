# src/schemas/base.py
from pydantic import BaseModel, ConfigDict

class BaseDTO(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="ignore",
        validate_assignment=True,
        # arbitrary_types_allowed=True,  # Удалите, если не используете свои типы
        from_attributes=True,
        allow_inf_nan=False,
        revalidate_instances="always",
        ser_json_timedelta="float",
        ser_json_bytes="base64",
        val_json_bytes="base64",
        validate_default=True,
        validate_return=True,
        regex_engine="python-re",
        populate_by_name=True,
    )
import re

from rest_framework.exceptions import ValidationError

FILTER_REGEX = re.compile(
    r"^filter(?P<ldelim>\[?)(?P<assoc>[\w\.\-]*)(?P<rdelim>\]?$)"
)


def parse_params_key(key):
    filtered_key = FILTER_REGEX.match(key)
    if filtered_key and (
            not filtered_key.groupdict()["assoc"]
            or filtered_key.groupdict()["ldelim"] != "["
            or filtered_key.groupdict()["rdelim"] != "]"
    ):
        raise ValidationError(f"invalid query parameter: {key}")
    if filtered_key:
        key_id = filtered_key.groupdict()["assoc"]
        return key_id
    return None

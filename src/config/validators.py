import os.path
from typing import Tuple

from .models import Settings, SettingType
from .utils import is_url_reachable

# ----------------------------------------------------------
# Custom Validators
# ----------------------------------------------------------

def song_storage_pattern_validator(value) -> Tuple[bool, str]:
    # Some logic here
    return True, "Song storage pattern validated successfully"

VALIDATORS = {
    'song_storage_pattern': song_storage_pattern_validator
}

def validate_setting(setting_name: str, value) -> Tuple[bool, str]:
    value = value.strip() if isinstance(value, str) else value

    try:
        setting_object = Settings.objects.get(name=setting_name)
    except Settings.DoesNotExist:
        raise ValueError(f'Setting with name "{setting_name}" not found')

    # Type-based validation
    if setting_object.type == SettingType.PATH:
        if not os.path.exists(value):
            return False, f'Path "{value}" does not exist'

    elif setting_object.type == SettingType.URL:
        if not is_url_reachable(value):
            return False, f'URL "{value}" is not reachable'

    # Custom validator
    validator_func = VALIDATORS.get(setting_object.name)
    if validator_func:
        return validator_func(value)

    return True, "Setting validated successfully"

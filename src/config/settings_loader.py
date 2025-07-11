import os
import json
from pathlib import Path
from .models import Settings, SettingType

def cast_env_value(env_value, setting_type):
    """Casts the environment variable string to the correct type."""
    if setting_type == SettingType.BOOL:
        return env_value.lower() in ("1", "true", "yes")
    elif setting_type == SettingType.INTEGER:
        return int(env_value)
    # For string, path, url, just return as is
    return env_value

def load_and_sync_settings():
    config_path = Path(__file__).parent / "settings.json"
    with open(config_path) as f:
        default_settings = json.load(f)

    for setting in default_settings:
        key = setting['name']
        default_value = setting['value']
        setting_type = setting.get('type', 'string')

        # Check for env override
        env_value = os.environ.get(key)
        value = cast_env_value(env_value, setting_type) if env_value is not None else default_value

        # Upsert all fields
        Settings.objects.update_or_create(
            name=key,
            defaults={
                'display_name': setting.get('display_name', key),
                'value': value,
                'description': setting.get('description', ''),
                'group': setting.get('group', 'General'),
                'type': setting_type,
            }
        )

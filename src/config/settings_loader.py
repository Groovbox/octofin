import os
import json
from pathlib import Path
from django.core.exceptions import ObjectDoesNotExist
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

    is_transient = os.environ.get("TRANSIENT_SETTINGS", "").lower() == "true"

    for setting in default_settings:
        key = setting['name']
        default_value = setting['value']
        setting_type = setting.get('type', 'string')

        # Get override from environment if present
        env_value = os.environ.get(key)
        value = cast_env_value(env_value, setting_type) if env_value is not None else default_value

        # Prepare common field values
        fields = {
            'display_name': setting.get('display_name', key),
            'value': value,
            'description': setting.get('description', ''),
            'group': setting.get('group', 'General'),
            'type': setting_type,
        }

        try:
            existing_obj = Settings.objects.get(name=key)
        except ObjectDoesNotExist:
            Settings.objects.create(name=key, **fields)
            continue

        if is_transient:
            for field, val in fields.items():
                setattr(existing_obj, field, val)
            existing_obj.save()
            continue

        # Compare only non-value fields to determine if update is needed
        needs_update = any(
            getattr(existing_obj, field) != val
            for field, val in fields.items()
            if field != 'value'  # 'value' is only updated when other fields differ
        )

        if needs_update:
            for field, val in fields.items():
                setattr(existing_obj, field, val)
            existing_obj.save()

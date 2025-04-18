# app/config.py
import os
from dynaconf import Dynaconf

ENV = os.getenv("ENV_FOR_DYNACONF", "dev")

settings = Dynaconf(
    environments=True,
    env_switcher="ENV_FOR_DYNACONF",
    settings_files=[
        "configs/settings.toml",                         # shared base
        f"configs/{ENV}/settings.toml",                  # env-specific settings
        "configs/.secrets.toml",                         # shared secrets
        f"configs/{ENV}/.secrets.toml",                  # env-specific secrets
    ],
)


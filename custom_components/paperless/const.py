"""Constants for the Paperless integration."""

from typing import Final

from homeassistant.const import CONF_URL

DEFAULT_NAME = "Paperless"
DOMAIN: Final = "paperless"

URL_PLACEHOLDER = {CONF_URL: "https://github.com/ViMaSter/hacs-paperless/blob/main/README.md"}

DATA_HASS_CONFIG = "paperless_hass_config"
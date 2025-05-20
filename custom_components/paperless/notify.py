"""Support for Paperless notification."""
import os

import voluptuous as vol

from homeassistant.components.notify import (
    PLATFORM_SCHEMA,
    BaseNotificationService,
)
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
import requests
import base64
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
type SolarlogConfigEntry = ConfigEntry[SolarLogCoordinator]

CONF_TIMESTAMP = "timestamp"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)

def get_service(hass: HomeAssistant,
    config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None,):
    """Get the paperless notification service."""

    return PaperlessNotificationService(hass, discovery_info[CONF_HOST], discovery_info[CONF_USERNAME], discovery_info[CONF_PASSWORD])


class PaperlessNotificationService(BaseNotificationService):
    """Implement the notification service for the paperless service."""

    def __init__(self, hass, host, username, password):
        """Initialize the service."""
        self.host = host
        self.username = username
        self.password = password

    def send_message(self, message="", **kwargs):
        """Send a message via a POST request."""

        # Prepare the authorization header
        auth_string = f"{self.username}:{self.password}"
        auth_header = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/json",
        }

        # Prepare the payload
        payload = {
            "documents": [1187],
            "method": "modify_custom_fields",
            "parameters": {
                "add_custom_fields": {2: str(dt_util.utcnow().isoformat())},
                "remove_custom_fields": {},
            },
        }

        # Send the POST request
        url = f"{self.host}/api/documents/bulk_edit/"
        response = requests.post(url, json=payload, headers=headers)

        # Log the response for debugging
        if response.status_code != 200:
            raise Exception(f"Failed to send message: {response.status_code} {response.text}")
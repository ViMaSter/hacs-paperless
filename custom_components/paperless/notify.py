"""Support for Paperless notification."""
import voluptuous as vol

from homeassistant.components.notify import (
    PLATFORM_SCHEMA,
    BaseNotificationService,
)
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
import requests
import base64
import logging
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
type SolarlogConfigEntry = ConfigEntry[SolarLogCoordinator]
from homeassistant.exceptions import HomeAssistantError
from .const import (
    DOMAIN
)

_LOGGER = logging.getLogger(__name__)

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
            "Authorization": f"Basic {auth_header}"
        }

        try:
            decodedPDF = base64.b64decode(message, validate=True)
        except base64.binascii.Error as e:
            _LOGGER.error("Message is not a base64-encoded message of a valid PDF\nReceived: %s\nException: %s", message, e)
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="Message is not a base64-encoded message of a valid PDF"
            )

        # Send the POST request
        files = {
            "document": ("document.pdf", decodedPDF, "application/pdf")
        }

        # Send the POST request
        url = f"{self.host}/api/documents/post_document/"
        response = requests.post(url, files=files, headers=headers)

        # Log the response for debugging
        if response.status_code != 200:
            _LOGGER.error("Paperless API returned non-200 status code: %s\n%s", response.status_code, response.text)
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="Paperless API returned non-200 status code; check logs for details",
            )
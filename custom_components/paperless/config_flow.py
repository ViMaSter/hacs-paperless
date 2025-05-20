"""Config flow for Paperless integration."""

from __future__ import annotations

from collections.abc import Mapping
import logging
from typing import Any

from aiohttp.client_exceptions import ClientConnectorError
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD, CONF_NAME

import base64
import aiohttp

from .const import DOMAIN, URL_PLACEHOLDER

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({vol.Required(CONF_HOST): str, vol.Required(CONF_USERNAME): str, vol.Required(CONF_PASSWORD): str})

class PaperlessFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Paperless."""

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> ConfigFlowResult:
        """Handle a reauthorization flow request."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, str, str] | None = None
    ) -> ConfigFlowResult:
        """Confirm reauth dialog."""
        errors = {}

        if user_input:
            while user_input and user_input[CONF_HOST].endswith("/"):
                user_input[CONF_HOST] = user_input[CONF_HOST][:-1]

            error = await _async_try_connect(user_input[CONF_HOST], user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
            key =f"{user_input[CONF_USERNAME]} @ {user_input[CONF_HOST]}"
            if not error and (entry := await self.async_set_unique_id(str(key))):
                return self.async_update_reload_and_abort(
                    entry, data=entry.data | user_input
                )
            
            errors["base"] = error

        user_input = user_input or {}
        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=CONFIG_SCHEMA,
            description_placeholders=URL_PLACEHOLDER,
            errors=errors,
        )

    async def async_step_user(
        self, user_input: dict[str, str, str] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initiated by the user."""
        errors = {}

        if user_input is not None:
            while user_input and user_input[CONF_HOST].endswith("/"):
                user_input[CONF_HOST] = user_input[CONF_HOST][:-1]

            error = await _async_try_connect(user_input[CONF_HOST], user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
            if error is None:
                key =f"{user_input[CONF_USERNAME]} @ {user_input[CONF_HOST]}"
                await self.async_set_unique_id(str(key))
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=key,
                    data=user_input | {CONF_NAME: key},
                )

            errors["base"] = error

        user_input = user_input or {}
        return self.async_show_form(
            step_id="user",
            data_schema=CONFIG_SCHEMA,
            description_placeholders=URL_PLACEHOLDER,
            errors=errors,
        )

    """ Returns a user-friendly error message, or None if the connection was successful """
    async def _async_try_connect(hostname: str, username: str, password: str) -> str | None:
        url = f"{hostname}/api/documents/?query=testquery"
        auth_header = base64.b64encode(f"{username}:{password}".encode()).decode()
        headers = {"Authorization": f"Basic {auth_header}"}

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        return f"Login failed: {response.status}: {response.text}"
                    data = await response.json()
                    if "count" not in data:
                        return f"Expected JSON with 'count' key; got: {response.text}"
                    return None
            except ClientConnectorError as ex:
                _LOGGER.exception("Connection error occurred: %s", ex)
                return f"Connection error: {ex}"
            except Exception as ex:
                _LOGGER.exception("An unknown error occurred: %s", ex)
                return f"Unknown error: {ex}"
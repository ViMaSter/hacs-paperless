# Paperless Home Assistant Notification

## Aim
Allows sending new documents from Home Assistant to Paperless-ngx via its REST API.

## Configuration
| Key | Type | Description |
| --- | --- | --- |
| `host` | `string` | The URL of your Paperless-ng instance (with or without trailing slash) |
| `username` | `string` | The username for Paperless-ng |
| `password` | `string` | The password for Paperless-ng |

Ensure the user has `Add` permission of type `Document` in Paperless-ng. (see also: [Paperless-ngx Documentation](https://docs.paperless-ngx.com/usage/#users-and-groups))

## Current Features
Sets the custom field of a predefined document to the current date and time.
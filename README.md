# Paperless Home Assistant Notification
[HACS](https://www.hacs.xyz/) component that enables sending new documents from Home Assistant to Paperless-ngx via its REST API.

## Installation
1. Clone this repository
2. Copy the contents of `custom_components` into your Home Assistant `config/custom_components` directory
3. Restart Home Assistant

## Setup
> [!NOTE]
> This component requires a Home Assistant instance that can access the Paperless-ngx instance.  
> This guide assumes that you have already set up Paperless-ngx and Home Assistant.

### Paperless-ngx
1. Open `/usersgroups` on your Paperless-ngx instance
2. Create a new user or select an existing user
3. Ensure the user has `Add` permission of type `Document` in Paperless-ng. (see also: [Paperless-ngx Documentation](https://docs.paperless-ngx.com/usage/#users-and-groups))
4. Copy the username and password of the user

### Home Assistant
1. Open `Settings`/`Devices & services`/`Add integration`
2. Search for and select `Paperless`
3. Enter these details:
   | Key | Type | Description |
   | --- | --- | --- |
   | `host` | `string` | The URL of your Paperless-ng instance (with or without trailing slash) |
   | `username` | `string` | The username for Paperless-ng |
   | `password` | `string` | The password for Paperless-ng |
4. Click `Submit`
5. Open `Settings`/`Automations & scenes`/`Create automation`
6. Select `Create new automation`
7. Under `Then do`, select `+ Add action`
8. Select `Notifications`/`Send a notification with {username}_{host}`
9. Base64 encode the PDF you want to send to Paperless-ngx
10. Paste any Base64 encoded PDF into the `message` field
11. Click the meatball menu in the top right corner and select `Run action`
12. Open the Paperless-ngx web interface and check if the document has been added
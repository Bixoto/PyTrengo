# PyTrengo

**PyTrengo** is a lightweight Python client for the Trengo API.

Note: PyTrengo is not affiliated nor endorsed by Trengo.

## Install

With pip:

    pip install pytrengo

With Poetry:

    poetry add pytrengo

Requirement: Python 3.10+

## Usage

```python3
from trengo import Trengo

trengo_client = Trengo(token="...")

# If the token is not provided, it’s read from the TRENGO_TOKEN environment variable
trengo_client = Trengo()

for ticket in trengo_client.get_tickets():
    print(...)
```

List queries are transparently paginated for you.

## Endpoints coverage

Note: even if an endpoint is not implemented, you can call it with one of the helper methods:

```python3
# GET /v2/some-endpoints?foo=bar
trengo_client.get_json_api("/some-endpoint", params={"foo": "bar"})
# POST /v2/some-other-endpoint with {"foo": "bar"}
trengo_client.post_json_api("/some-other-endpoint",
                            json={"foo": "bar"})
```

| Endpoint                           | Method                                   |
|:-----------------------------------|:-----------------------------------------|
| **All endpoints (43%)**            |                                          |
| **Tickets**                        |                                          |
| List all tickets                   | `get_tickets`                            |
| List all aggregates                | `get_ticket_aggregates`                  |
| Create a ticket                    | `create_ticket`                          |
| Assign a ticket                    | `assign_ticket`                          |
| Close a ticket                     | `close_ticket`                           |
| Reopen a ticket                    | `reopen_ticket`                          |
| Merge a ticket                     | `merge_ticket`                           |
| Attach a label                     | `attach_ticket_label`                    |
| Detach a label                     | `detach_ticket_label`                    |
| Delete a ticket                    | `delete_ticket`                          |
| Mark as spam                       | `mark_ticket_as_spam`                    |
| Unmark as spam                     | `unmark_ticket_as_spam`                  |
| Set custom data                    | `set_custom_data`                        |
| Delete a message                   | `delete_message`                         |
| Send a ticket message              | `send_ticket_message`                    |
| Send a ticket media message        | `send_ticket_media_message`              |
| List all messages                  | `get_messages`                           |
| Mark a ticket as favorite          | `mark_ticket_as_favorite`                |
| Unmark a ticket as favorite        | `unmark_ticket_as_favorite`              |
| Fetch a message                    | `get_message`                            |
| Store a custom channel message     | `store_custom_channel_message`           |
| **WhatsApp**                       |                                          |
| Send a WhatsApp template           | `send_whatsapp_template`                 |
| **Contacts**                       |                                          |
| List contacts                      | `get_contacts`                           |
| View a contact                     | `get_contact`                            |
| Create a contact                   | `create_contact`                         |
| Update a contact                   | `update_contact`                         |
| Delete a contact                   | `delete_contact` (since 0.1.5)           |
| Custom fields                      | `set_contact_custom_field` (since 0.1.5) |
| Add a note                         | `add_contact_note` (since 0.1.5)         |
| Delete a note                      | `delete_contact_note` (since 0.1.5)      |
| **Profiles (16%)**                 |
| Create a profile                   |                                          |
| List profiles                      | `get_profiles`                           |
| View a profile                     | `get_profile`                            |
| Update a profile                   |                                          |
| Custom fields                      |                                          |
| Delete a profile                   |                                          |
| Create a note                      |                                          |
| Delete a note                      |                                          |
| Attach a contact                   |                                          |
| Detach a contact                   |                                          |
| Set profile image                  |                                          |
| Unset profile image                |                                          |
| **SMS messages (33%)**             |
| List all messages                  | `get_sms_messages`                       |
| Send a message                     |                                          |
| Fetch balance                      |                                          |
| **Messages (0%)**                  |
| Import text message                |                                          |
| Import email message               |                                          |
| **Team Chat (0%)**                 |
| Sending a bot message              |                                          |
| **Voip (0%)**                      |
| Push SIP call status               |                                          |
| List all voip calls                |                                          |
| Get a voip call                    |                                          |
| **Help Center (24%)**              |
| List all help centers              | `get_help_centers`                       |
| List all categories                | `get_help_center_categories`             |
| List all articles                  |                                          |
| List all blocks                    | `get_help_center_blocks`                 |
| Get a help center                  | `get_help_center`                        |
| Get a category                     | `get_help_center_category`               |
| Get an article                     | `get_help_center_article`                |
| Get a block                        | `get_help_center_block`                  |
| Create a help center               |                                          |
| Create a category                  |                                          |
| Create a section                   |                                          |
| Create an article                  |                                          |
| Create a block                     |                                          |
| Update a help center               |                                          |
| Update a category                  |                                          |
| Update a section                   |                                          |
| Update an article                  |                                          |
| Update a block                     |                                          |
| Delete a help center               | `delete_help_center`                     |
| Delete a category                  | `delete_help_center_category`            |
| Delete a section                   |                                          |
| Delete an article                  |                                          |
| Delete a block                     |                                          |
| **Quick Replies (20%)**            |
| List all quick replies             | `get_quick_replies`                      |
| Create a quick reply               |                                          |
| Update a quick reply               |                                          |
| Delete a quick reply               |                                          |
| **Ticket Results (20%)**           |
| List all ticket results            | `get_ticket_results`                     |
| Get a ticket result                |                                          |
| Create a ticket result             |                                          |
| Update a ticket result             |                                          |
| Delete a ticket result             |                                          |
| **Contact Groups (20%)**           |
| List all contact groups            | `get_contact_groups`                     |
| Get a contact group                |                                          |
| Create a contact group             |                                          |
| Update a contact group             |                                          |
| Delete a contact group             |                                          |
| **Labels (20%)**                   |
| List all labels                    | `get_labels`                             |
| Get a label                        |                                          |
| Create a label                     |                                          |
| Update a label                     |                                          |
| Delete a label                     |                                          |
| **Teams (20%)**                    |
| List all teams                     | `get_teams`                              |
| Get a team                         |                                          |
| Update a team                      |                                          |
| Create a team                      |                                          |
| Delete a team                      |                                          |
| **Users (20%)**                    |
| List all users                     | `get_users`                              |
| Get a user                         |                                          |
| Create a user                      |                                          |
| Update a user                      |                                          |
| Delete a user                      |                                          |
| **Custom fields (20%)**            |
| List all custom fields             | `get_custom_fields`                      |
| Create a custom field              |                                          |
| Get a custom field                 |                                          |
| Update a custom field              |                                          |
| Delete a custom field              |                                          |
| **Webhooks (60%)**                 |
| List all webhooks                  | `get_webhooks`                           |
| Create a webhook                   | `create_webhook`                         |
| Get a webhook                      | `get_webhook`                            |
| Update a webhook                   |                                          |
| Delete a webhook                   |                                          |
| **Quick actions (0%)**             |
| Send a message                     |                                          |
| Log a phone call                   |                                          |
| **BETA - Reporting (20%)**         |
| BETA - Get reporting metrics       | `get_reporting_metrics`                  |
| BETA - Get user report             |                                          |
| BETA - Get reporting histograms    |                                          |
| BETA - Agent performance reporting |                                          |
| BETA - Get Ticket Details Report   |                                          |

## Naming

We follow the naming used in the Trengo API, but we sometimes have to differ from it for consistency or to follow Python
conventions:

* Methods for API endpoints like "List &lt;name>s" are named `get_<name>s`
* Methods for API endpoints like "Get &lt;name>" or "View &lt;name>" are named `get_<name>`
* We try to stay consistent even when the API isn’t: the field for the relations to include is always named `include` in
  PyTrengo, while the API uses `include` in some calls and `with` in some others
* Some endpoints take a single ID; their method use an extended name like `contact_id` or `ticket_id` instead of `id`

## License

Copyright 2024 [Bixoto](https://bixoto.com/).

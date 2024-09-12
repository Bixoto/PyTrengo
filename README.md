# PyTrengo

**PyTrengo** is a lightweight Python client for the Trengo API.

Note: PyTrengo is not affiliated nor endorsed by Trengo.

## Install

With pip:

    pip install pytrengo

With Poetry:

    poetry add pytrengo

Requirement: Python 3.10+

## Endpoints coverage

Note: even if an endpoint is not implemented, you can call it with one of the helper methods:

```python
trengo_client.get_json_api("/some-endpoint", params={"foo": "bar"})  # calls GET /v2/some-endpoints?foo=bar
trengo_client.post_json_api("/some-other-endpoint",
                            json={"foo": "bar"})  # calls POST /v2/some-other-endpoint with {"foo": "bar"}
```

| Endpoint                           | Method                  |
|:-----------------------------------|:------------------------|
| **All endpoints**                  | **12%**                 |
| **Tickets**                        | **0%**                  |
| List all tickets                   |                         |
| List all aggregates                |                         |
| Create a ticket                    |                         |
| Assign a ticket                    |                         |
| Close a ticket                     |                         |
| Reopen a ticket                    |                         |
| Merge a ticket                     |                         |
| Attach a label                     |                         |
| Detach a label                     |                         |
| Delete a ticket                    |                         |
| Mark as spam                       |                         |
| Unmark as spam                     |                         |
| Set custom data                    |                         |
| Delete a message                   |                         |
| Send a ticket message              |                         |
| Send a ticket media message        |                         |
| List all messages                  |                         |
| Mark a ticket as favorite          |                         |
| Unmark a ticket as favorite        |                         |
| Fetch a message                    |                         |
| Store a custom channel message     |                         |
| **WhatsApp**                       | **0%**                  |
| Send a WhatsApp template           |                         |
| **Contacts**                       | **12%**                 |
| List contacts                      | `get_contacts`          |
| View a contact                     |                         |
| Create a contact                   |                         |
| Update a contact                   |                         |
| Delete a contact                   |                         |
| Custom fields                      |                         |
| Add a note                         |                         |
| Delete a note                      |                         |
| **Profiles**                       | **8%**                  |
| Create a profile                   |                         |
| List profiles                      | `get_profiles`          |
| View a profile                     |                         |
| Update a profile                   |                         |
| Custom fields                      |                         |
| Delete a profile                   |                         |
| Create a note                      |                         |
| Delete a note                      |                         |
| Attach a contact                   |                         |
| Detach a contact                   |                         |
| Set profile image                  |                         |
| Unset profile image                |                         |
| **SMS messages**                   | **33%**                 |
| List all messages                  | `get_sms_messages`      |
| Send a message                     |                         |
| Fetch balance                      |                         |
| **Messages**                       | **0%**                  |
| Import text message                |                         |
| Import email message               |                         |
| **Team Chat**                      | **0%**                  |
| Sending a bot message              |                         |
| **Voip**                           | **0%**                  |
| Push SIP call status               |                         |
| List all voip calls                |                         |
| Get a voip call                    |                         |
| **Help Center**                    | **4%**                  |
| List all help centers              | `get_help_centers`      |
| List all categories                |                         |
| List all articles                  |                         |
| List all blocks                    |                         |
| Get a help center                  |                         |
| Get a category                     |                         |
| Get an article                     |                         |
| Get a block                        |                         |
| Create a help center               |                         |
| Create a category                  |                         |
| Create a section                   |                         |
| Create an article                  |                         |
| Create a block                     |                         |
| Update a help center               |                         |
| Update a category                  |                         |
| Update a section                   |                         |
| Update an article                  |                         |
| Update a block                     |                         |
| Delete a help center               |                         |
| Delete a category                  |                         |
| Delete a section                   |                         |
| Delete an article                  |                         |
| Delete a block                     |                         |
| **Quick Replies**                  | **20%**                 |
| List all quick replies             | `get_quick_replies`     |
| Create a quick reply               |                         |
| Update a quick reply               |                         |
| Delete a quick reply               |                         |
| **Ticket Results**                 | **20%**                 |
| List all ticket results            | `get_ticket_results`    |
| Get a ticket result                |                         |
| Create a ticket result             |                         |
| Update a ticket result             |                         |
| Delete a ticket result             |                         |
| **Contact Groups**                 | **20%**                 |
| List all contact groups            | `get_contact_groups`    |
| Get a contact group                |                         |
| Create a contact group             |                         |
| Update a contact group             |                         |
| Delete a contact group             |                         |
| **Labels**                         | **20%**                 |
| List all labels                    | `get_labels`            |
| Get a label                        |                         |
| Create a label                     |                         |
| Update a label                     |                         |
| Delete a label                     |                         |
| **Teams**                          | **20%**                 |
| List all teams                     | `get_teams`             |
| Get a team                         |                         |
| Update a team                      |                         |
| Create a team                      |                         |
| Delete a team                      |                         |
| **Users**                          | **20%**                 |
| List all users                     | `get_users`             |
| Get a user                         |                         |
| Create a user                      |                         |
| Update a user                      |                         |
| Delete a user                      |                         |
| **Custom fields**                  | **20%**                 |
| List all custom fields             | `get_custom_fields`     |
| Create a custom field              |                         |
| Get a custom field                 |                         |
| Update a custom field              |                         |
| Delete a custom field              |                         |
| **Webhooks**                       | **60%**                 |
| List all webhooks                  | `get_webhooks`          |
| Create a webhook                   | `create_webhook`        |
| Get a webhook                      | `get_webhook`           |
| Update a webhook                   |                         |
| Delete a webhook                   |                         |
| **Quick actions**                  | **0%**                  |
| Send a message                     |                         |
| Log a phone call                   |                         |
| **BETA - Reporting**               | **20%**                 |
| BETA - Get reporting metrics       | `get_reporting_metrics` |
| BETA - Get user report             |                         |
| BETA - Get reporting histograms    |                         |
| BETA - Agent performance reporting |                         |
| BETA - Get Ticket Details Report   |                         |
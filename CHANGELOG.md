# PyTrengo Changelog

## 0.1.3 (2024/09/13)

* Make `get_profiles`’s and `get_contacts`’s `term` argument optional
* Add `attach_ticket_label`, `detach_ticket_label`, `delete_ticket`, `set_custom_data`, `delete_message`,
  `send_ticket_message`, `send_ticket_media_message` (untested), `get_messages`, `get_message`,
  `store_custom_channel_message` (untested)
* Add type hints on `get_webhook`, `get_help_center`, `get_help_center_category`, `get_help_center_article`,
  `get_help_center_block`

## 0.1.2 (2024/09/12)

* Fix the date parameters serialization (again)
* Add `assign_ticket`, `assign_ticket_to_user`, `assign_ticket_to_team`, `close_ticket`, `reopen_ticket`, `merge_ticket`

## 0.1.1 (2024/09/12)

* Add `get_tickets`, `get_ticket_aggregates`, `create_ticket`, `mark_ticket_as_spam`, `mark_ticket_as_favorite`,
  `unmark_ticket_as_favorite`
* Add `get_help_center_categories`, `get_help_center_blocks`, `get_help_center`, `get_help_center_category`,
  `get_help_center_article`, `get_help_center_block`, `delete_help_center`, `delete_help_center_category`
* Add `send_whatsapp_template`

## 0.1.0 (2024/09/12)

* Fix the date parameters serialization
* Add `create_webhook`, `get_webhook`
* Pass additional keyword arguments to the `APISession` constructor
* Remove the `python-dotenv` dependency

## 0.1.0-alpha1 (2024/09/11)

Initial release.
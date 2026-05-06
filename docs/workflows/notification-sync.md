# Notification Sync Workflow

Purpose:
Accept a webhook payload for notification-oriented or sync-oriented automation.

Why this workflow starts simple:
- First we fix a stable webhook contract.
- Later this flow can fan out to Telegram, Slack, CRM, or scheduled jobs.
- A lightweight webhook is easier to validate than a full external integration.

Steps:
1. Receive a JSON payload through `POST /webhook/notification-sync`
2. Return a JSON acknowledgement through `Respond to Webhook`

Expected success response:
```json
{
  "status": "accepted",
  "workflow": "notification-sync",
  "document_id": "DOCUMENT_ID",
  "message": "Notification payload received"
}
```

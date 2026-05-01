# assignment-tracker

Assignment tracker API backed by Google Sheets.

## Gemini integration

This project now includes a Gemini-powered endpoint that suggests assignment priority:

- `POST /suggest-priority`
- request body: `{ "assignment": "Finish chapter 5 and submit by Monday" }`
- response: `{ "priority": "High", "reason": "Near deadline and graded submission." }`

Create a `.env` file in the project root:

```powershell
GEMINI_API_KEY=your-api-key
GOOGLE_SERVICE_ACCOUNT_TYPE=service_account
GOOGLE_SERVICE_ACCOUNT_PROJECT_ID=...
GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY_ID=...
GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
GOOGLE_SERVICE_ACCOUNT_CLIENT_EMAIL=...
GOOGLE_SERVICE_ACCOUNT_CLIENT_ID=...
GOOGLE_SERVICE_ACCOUNT_AUTH_URI=https://accounts.google.com/o/oauth2/auth
GOOGLE_SERVICE_ACCOUNT_TOKEN_URI=https://oauth2.googleapis.com/token
GOOGLE_SERVICE_ACCOUNT_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
GOOGLE_SERVICE_ACCOUNT_CLIENT_X509_CERT_URL=...
GOOGLE_SERVICE_ACCOUNT_UNIVERSE_DOMAIN=googleapis.com
```

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
```

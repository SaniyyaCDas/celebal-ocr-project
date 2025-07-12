# celebal-ocr-project
celebal project

# CELEBAL Internship Project – OCR on Blob Images with Azure Functions

This project extracts handwritten or printed text from images uploaded to Azure Blob Storage using Azure's Computer Vision API. Once processed, it saves the output as a JSON file and sends an email notification — all triggered automatically.

---

## Features
- Fetch image from Azure Blob (`input-container`)
- Extract text using Azure Computer Vision OCR
- Store results in JSON format in `output-container`
- Send email alert after processing
- Accessible on private network only
- Fully automated on blob upload

---

## Tech Stack
- Python (Azure Function)
- Azure Blob Storage
- Azure AI Vision API
- Email SMTP (or SendGrid)

---

## Project Structure
```
celebal-ocr-project/
├── main_function/
│   ├── __init__.py
│   └── function.json
├── requirements.txt
├── local.settings.json
└── README.md
```

---

## Setup Instructions

### 1. Replace Placeholder Configs
Edit `local.settings.json` with your actual values:

```json
"COMPUTER_VISION_KEY": "<your_key_here>",
"AzureWebJobsStorage": "<your_connection_string>",
"EMAIL_USER": "<your_email>",
"EMAIL_PASS": "<your_password>"
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Run the Azure Function Locally
Install Azure Functions Core Tools:
https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local

Then run:
```bash
func start
```

---

## Security Note
Do not commit real API keys, passwords, or connection strings. Use placeholder values in public repositories and configure secrets in your local or cloud environment.

---

## Email Configuration
To enable email notifications using Gmail SMTP:
- Enable app passwords (recommended)
- Add these to `local.settings.json`:
```json
"EMAIL_USER": "your_email@gmail.com",
"EMAIL_PASS": "your_app_password"
```

---

## Submission Guidelines
- Do not include ZIP files
- Maintain the directory structure shown above
- Provide a clean and working repository with placeholder secrets

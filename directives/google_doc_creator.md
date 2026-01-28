# Google Doc Creator (Standalone Utility)

## What This Workflow Is
**Standalone utility workflow** that can be called by ANY agentic workflow. Creates formatted Google Docs from Markdown with proper styling (headers, bold, bullets). Reusable across all directives.

## What It Does
1. Receives Markdown content and metadata
2. Converts Markdown to Google Docs format
3. Applies standard formatting (headings, bullets, bold, etc.)
4. Creates document in specified folder
5. Sets sharing permissions
6. Returns shareable link

## Prerequisites

### Required Files
```
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Installation
```bash
pip install google-api-python-client google-auth
```

## Inputs
- `content` (string): Markdown content
- `title` (string): Document title
- `folderId` (string, optional): Google Drive folder ID
- `shareWith` (array, optional): Email addresses to share with

## Process
1. Authenticate with Google API
2. Convert Markdown to Google Docs formatting
3. Create document via Google Docs API
4. Apply text formatting (bold, headings, lists)
5. Move to specified folder (or create client folder)
6. Set sharing permissions (link sharing or specific emails)
7. Return document ID and shareable URL

## Outputs
```json
{
  "documentId": "abc123",
  "documentUrl": "https://docs.google.com/document/d/abc123/edit",
  "title": "Acme Corp - VSL Script",
  "createdAt": "2026-01-05T12:00:00Z"
}
```

## Integration
Position 5/7 in VSL funnel pipeline. Used by multiple workflows for document delivery.

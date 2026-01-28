# Formatted Google Doc Creator

> **Status:** ✅ Active | **Last Updated:** January 7, 2026

## What This Workflow Is
A centralized, reusable workflow that creates perfectly formatted Google Docs from markdown content. Uses native Google Docs API formatting (headings, bold, italic, bullets, links) instead of displaying raw markdown text.

## What It Does
1. Accepts markdown content
2. Parses and extracts formatting (headers, bold, italic, code, links, bullets)
3. Creates Google Doc with proper native formatting
4. Optionally moves to specified folder
5. Optionally sends Slack notification

## Why Use This
- **Consistent formatting** across all workflows
- **Single source of truth** - update once, applies everywhere
- **Native Google Docs styling** - not markdown text
- **Reusable module** - import into any workflow

## Supported Formatting

| Markdown | Google Docs Output |
|----------|-------------------|
| `# Heading 1` | Heading 1 style |
| `## Heading 2` | Heading 2 style |
| `### Heading 3` | Heading 3 style |
| `**bold**` | Bold text |
| `*italic*` | Italic text |
| `` `code` `` | Monospace font with gray background |
| `[link](url)` | Clickable hyperlink (blue) |
| `- item` | Bullet point (•) |
| `---` | Horizontal rule |

## Prerequisites

### Required
- Google OAuth credentials (`credentials.json` or `token_docs.json`)
- Python 3.10+

### Optional
- `SLACK_BOT_TOKEN` - For notifications
- `SLACK_CONTENT_CHANNEL_ID` - Channel for notifications

## How to Run

### CLI
```bash
# From markdown file
python3 execution/create_formatted_google_doc.py \
  --content "path/to/content.md" \
  --title "Document Title" \
  --folder-id "optional_folder_id" \
  --notify

# Test mode (creates sample doc with all formatting)
python3 execution/create_formatted_google_doc.py --test
```

### Programmatic (Import)
```python
from execution.create_formatted_google_doc import create_formatted_doc

result = create_formatted_doc(
    title="My Document",
    content="# Header\n\nThis is **bold** and *italic*.",
    folder_id="optional_folder_id",
    notify_slack=True
)

print(result["documentUrl"])
```

## Inputs
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Document title |
| content | string | Yes | Markdown content |
| folder_id | string | No | Google Drive folder ID |
| notify_slack | bool | No | Send Slack notification |

## Output
```json
{
  "documentId": "abc123...",
  "documentUrl": "https://docs.google.com/document/d/abc123.../edit",
  "title": "Document Title",
  "status": "created"
}
```

## Integration Example

To use in other workflows:

```python
# In your workflow script
from create_formatted_google_doc import create_formatted_doc

# Generate your content
content = generate_email_flow(...)

# Create formatted doc
result = create_formatted_doc(
    title=f"{brand_name} - Email Flow",
    content=content,
    folder_id=client_folder_id,
    notify_slack=True
)

# Use the URL
doc_url = result["documentUrl"]
```

## Error Handling
| Scenario | Behavior |
|----------|----------|
| No credentials | Returns status: "no_credentials" |
| Invalid range | Filters out, continues with valid formatting |
| API error | Returns status: "error" with message |
| Slack fails | Logs warning, continues |

## Related Files
- `execution/create_formatted_google_doc.py` - Main script
- `execution/create_google_doc.py` - Legacy version (basic formatting)

## Workflows That Should Use This
- Email Flow Writer
- VSL Funnel Generator
- Case Study Generator
- Proposal Creator
- QBR Generator
- Monthly Reporting
- Any workflow creating Google Docs

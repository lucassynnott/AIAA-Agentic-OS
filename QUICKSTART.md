# AIAA Agentic OS - Quick Start Guide

## Prerequisites

1. **VS Code** with Claude Code extension installed
2. **Python 3.10+** installed on your system
3. **API Keys** for the services you want to use (see `.env.example`)

---

## Setup (2 minutes)

### Step 1: Open in VS Code
Open this folder in VS Code with the Claude Code extension active.

### Step 2: Ask Claude to Set You Up
In the Claude Code chat, type:

> "Set up my environment for the Agentic OS"

Claude will:
- Create a Python virtual environment
- Install all dependencies from `requirements.txt`
- Create your `.env` file from the template
- Walk you through adding your API keys

### Step 3: Add Your API Keys
Claude will ask you for each API key. Have these ready:
- **Anthropic API Key** (required) - from console.anthropic.com
- **Apify Token** (for lead scraping) - from console.apify.com
- **Google OAuth** (for Sheets) - follow Claude's instructions

---

## Using the System

### Running a Workflow

Ask Claude to run any directive:

> "Run the cold email scriptwriter workflow"

> "Help me scrape leads for plumbers in Miami"

> "Create a proposal for [client name]"

### Available Workflows

**Cold Email:**
- Cold Email Scriptwriter
- Cold Email Mass Personalizer
- Automated Prospecting + GHL CRM
- Daily Campaign Reports
- Domain Health Analyzer

**Funnels & Ads:**
- Landing Page CRO Analyzer
- VSL Funnel Writer
- Webinar Funnel Generator
- Static Ad Generator
- Facebook Ad Library Analysis

**E-commerce Email:**
- Email Flow Writer
- Campaign Generator
- Content Calendar Generator

**Content:**
- YouTube Script Creator
- RSS-to-Content Pipeline
- Zoom Call Content Repurposer

### Listing All Directives

> "Show me all available directives"

Or browse the `directives/` folder.

---

## How It Works

This system uses a 3-layer architecture:

1. **Directives** (`directives/`) - SOPs that tell Claude what to do
2. **Orchestration** (Claude) - Makes decisions, routes tasks
3. **Execution** (`execution/`) - Python scripts that do the actual work

When you ask Claude to do something, it:
1. Finds the relevant directive
2. Reads the instructions
3. Runs the appropriate execution scripts
4. Returns results to you

---

## Troubleshooting

### "Module not found" errors
Ask Claude: "Reinstall my dependencies"

### Google Sheets not working
Ask Claude: "Help me set up Google OAuth"

### API errors
Ask Claude: "Check my .env file for [service name]"

---

## Need Help?

Just ask Claude! It has access to all directives and can explain how any workflow works.

# Zoom Call > Multi Content Copywriter + Scheduler

## What This Workflow Is
This workflow processes Zoom call recordings to generate multiple content pieces (social posts, blog summaries, video clips) and schedules them.

## What It Does
1. Receives Zoom recording/transcript
2. Extracts key insights and quotes
3. Generates LinkedIn, Twitter, blog posts
4. Creates video clip suggestions
5. Schedules content across platforms

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Installation
```bash
pip install openai google-api-python-client
```

## How to Run
```bash
python3 execution/zoom_to_content.py --transcript "[TRANSCRIPT_PATH]" --platforms "linkedin,twitter,blog"
```

## Goal
This workflow uses AI to process inputs and generate structured outputs.

## Trigger
- **Type**: Manual
- **Node**: Manual Trigger

## Inputs
- [Define inputs based on trigger type]

## Integrations Required
- Anthropic
- Slack
- Google Sheets

## Process
### 1. YouTube Script Agent
AI agent processes the input with the following instructions:
```
=GOAL:
Write a high-converting YouTube video script based on the following transcript.

Use a natural, persuasive tone. Begin with a strong hook that includes proof, a promise, and a brief plan. Then walk through 2–3 teaching segments. End with a clear summary and call-to-action.

FORMATTING:
First, break up the different sentences/paragraphs into their own lines as needed, rather than grouping many sentences into the same paragraph.

Second, format the entire script within this template:

Hook:

Proof – Why you’re credible

Promise – What the viewer will get

Plan – How you’ll deliver it

Persona – Who this is for (explicitly or implicitly)

... [truncated]
```

### 2. YT Script Doc Title Agent
AI agent processes the input with the following instructions:
```
=Turn the YouTube video script below into a 3–7 word title that we can insert as the title for the document that has this YouTube video script inside of it.

!IMPORTANT: Don’t respond with ANYTHING other than the completed 3–7 word title. That 3–7 word title should be the only thing in your response.

The YouTube video script:

{{ $json.output }}
```

### 3. LinkedIn Post Agent
AI agent processes the input with the following instructions:
```
=GOAL:
Take the transcript below from a Zoom call where I, Lucas Synnott, spoke in-depth about a specific topic, and turn it into a LinkedIn post. Remember that I am Lucas Synnott and I'm writing in the first person.

Use the contents of that transcript, combined with your system knowledge, to create a high-performing LinkedIn post.

FORMATTING:
Format the output according to the LinkedIn frameworks provided, including a strong hook, clear structure, and engaging conclusion.

The post should be purely text based.

WARNINGS:
Write the copy in the voice and character that myself, Lucas Synnott, would have when writing content. It sounds real, natural, and like something that I would use in a real human-to-human conversation as the owner of a marketing agency.

In your response, don’t include ANY formatting or odd characters, just text only. Don’t include any of the following in your response, unless it is part of the text of the script: #, *, **

In your response, be sure to ONLY reply with the post copy, don’t include other text or explanations.

TRANSCRIPT:

{{ $json.body.transcript.plaintext }}
... [truncated]
```

### 4. LinkedIn Post(s) Doc Title Agent
AI agent processes the input with the following instructions:
```
=Turn the Linkedin post below into a 3–7 word title that we can insert as the title for the document that has this Linkedin post inside of it.

!IMPORTANT: Don’t respond with ANYTHING other than the completed 3–7 word title. That 3–7 word title should be the only thing in your response.

The YouTube video script:

{{ $json.output }}
```

### 5. Email Newsletter Agent
AI agent processes the input with the following instructions:
```
=GOAL:
Take this transcript from a Zoom call where Lucas spoke in-depth about a specific topic. Turn the key insights from this transcript into a single email newsletter in the style of Lucas’s existing writing.

The final output should:

Be emotionally resonant, not overly polished

Feel personal, like it’s coming from Lucas directly

Reflect the tone and structure of past AI Agency Academy newsletters

End with a soft sign-off in Lucas’s typical voice

FORMATTING:
[!IMPORTANT] Include appropriate formatting and line breaks.

In your response, ONLY include the copy for the newsletter. Do not include any other words, context, or explanations.

Do not generate a title for the newsletter. You are an agent that ONLY creates the body of the newsletter, another agent is in charge of titling it.

... [truncated]
```

### 6. Email Newsletter Doc Title Agent
AI agent processes the input with the following instructions:
```
=Turn the email newsletter document below into a 3–7 word title that we can insert as the title for the document that has the email copy inside of it. Do not include : anywhere in the title.

!IMPORTANT: Don't respond with ANYTHING other than the completed 3–7 word title. That 3–7 word title should be the only thing in your response.

The YouTube video script:

{{ $json.output }}







```

### 7. HTTP Request
[Describe what this step does]

### 8. Google Drive
[Describe what this step does]

### 9. HTTP Request1
[Describe what this step does]

### 10. Google Drive1
[Describe what this step does]

### 11. HTTP Request2
[Describe what this step does]

### 12. Google Drive2
[Describe what this step does]

### 13. OpenRouter Chat Model
[Describe what this step does]

### 14. OpenRouter Chat Model1
[Describe what this step does]

### 15. Slack
[Describe what this step does]

### 16. Slack1
[Describe what this step does]

### 17. HTTP Request3
[Describe what this step does]

### 18. Google Drive3
[Describe what this step does]

### 19. Slack2
[Describe what this step does]

### 20. Twitter Post Agent
AI agent processes the input with the following instructions:
```
=GOAL:
Take the transcript below from a Zoom call where I, Lucas Synnott, spoke in-depth about a specific topic, and turn it into a tweet. Remember that I am Lucas Synnott and I'm writing in the first person.

Use the contents of that transcript, combined with your system knowledge, to create a high-performing twitter post.

FORMATTING:
Format the output according to the twitter frameworks provided, including a strong hook, clear structure, and engaging conclusion.

The post should be purely text based.

WARNINGS:
Write the copy in the voice and character that myself, Lucas Synnott, would have when writing content. It sounds real, natural, and like something that I would use in a real human-to-human conversation as the owner of a marketing agency.

In your response, don’t include ANY formatting or odd characters, just text only. Don’t include any of the following in your response, unless it is part of the text of the script: #, *, **

In your response, be sure to ONLY reply with the post copy, don’t include other text or explanations.

TRANSCRIPT:

{{ $json.body.transcript.plaintext }}
... [truncated]
```

### 21. Twitter Post(s) Doc Title Agent
AI agent processes the input with the following instructions:
```
=Turn the Tweet post below into a 3–7 word title that we can insert as the title for the document that has this Linkedin post inside of it.

!IMPORTANT: Don’t respond with ANYTHING other than the completed 3–7 word title. That 3–7 word title should be the only thing in your response.

The tweet:

{{ $json.output }}
```

### 22. Slack3
[Describe what this step does]

### 23. OpenRouter Chat Model2
[Describe what this step does]

### 24. Prepare LinkedIn Content for Queue
Data is normalized/transformed for the next step.

### 25. Prepare Newsletter Content for Queue
Data is normalized/transformed for the next step.

### 26. Prepare Twitter Content for Queue
Data is normalized/transformed for the next step.

### 27. Add LinkedIn to Content Queue
[Describe what this step does]

### 28. Add LinkedIn to Content Queue1
[Describe what this step does]

### 29. Prepare LinkedIn Content for Queue1
Data is normalized/transformed for the next step.

### 30. Add YouTube to Content Queue
[Describe what this step does]

### 31. When chat message received
Workflow is triggered via manual.

### 32. Publish Newsletter to ConvertKit
[Describe what this step does]

### 33. Google Docs
[Describe what this step does]

### 34. Code
[Describe what this step does]

### 35. Extract LinkedIn IDs
Data is normalized/transformed for the next step.

### 36. Set Post Content1
Data is normalized/transformed for the next step.

### 37. Code1
[Describe what this step does]

### 38. Add Twitter to Content Queue
[Describe what this step does]

### 39. Set Post Content
Data is normalized/transformed for the next step.

### 40. Code2
[Describe what this step does]

### 41. Extract Twitter IDs
Data is normalized/transformed for the next step.

### 42. Linkedin Automation Done
Data is normalized/transformed for the next step.

### 43. Twitter Automation Done
Data is normalized/transformed for the next step.

### 44. Linkedin Post Approved?
[Describe what this step does]

### 45. Twitter Post Approved?
[Describe what this step does]

### 46. Newsletter Post Approved?
[Describe what this step does]

### 47. Newsletter Automation Done
Data is normalized/transformed for the next step.

### 48. [Instagram] Publish via Blotato
[Describe what this step does]

### 49. [Facebook] Publish via Blotato
[Describe what this step does]

### 50. [Linkedin] Publish via Blotato
[Describe what this step does]

### 51. [Tiktok] Publish via Blotato
[Describe what this step does]

### 52. [Youtube] Publish via Blotato
[Describe what this step does]

### 53. [Threads] Publish via Blotato
[Describe what this step does]

### 54. [Twitter] Publish via Blotato
[Describe what this step does]

### 55. [Bluesky] Publish via Blotato
[Describe what this step does]

### 56. Prepare for Publish
Data is normalized/transformed for the next step.

### 57. HTTP Request4
[Describe what this step does]

### 58. Google Drive4
[Describe what this step does]

### 59. Slack4
[Describe what this step does]

### 60. Prepare Twitter Content for Queue1
Data is normalized/transformed for the next step.

### 61. Add Twitter to Content Queue1
[Describe what this step does]

### 62. Twitter Automation Done1
Data is normalized/transformed for the next step.

### 63. Twitter Post Approved?1
[Describe what this step does]

### 64. Facebook Post Agent
AI agent processes the input with the following instructions:
```
=GOAL:
Take the transcript below from a Zoom call where I, Lucas Synnott, spoke in-depth about a specific topic, and turn it into a tweet. Remember that I am Lucas Synnott and I'm writing in the first person.

Use the contents of that transcript, combined with your system knowledge, to create a high-performing twitter post.

FORMATTING:
Format the output according to the twitter frameworks provided, including a strong hook, clear structure, and engaging conclusion.

The post should be purely text based.

WARNINGS:
Write the copy in the voice and character that myself, Lucas Synnott, would have when writing content. It sounds real, natural, and like something that I would use in a real human-to-human conversation as the owner of a marketing agency.

In your response, don’t include ANY formatting or odd characters, just text only. Don’t include any of the following in your response, unless it is part of the text of the script: #, *, **

In your response, be sure to ONLY reply with the post copy, don’t include other text or explanations.

TRANSCRIPT:

{{ $json.body.transcript.plaintext }}
... [truncated]
```

### 65. Facebook Post Title Agent
AI agent processes the input with the following instructions:
```
=Turn the Tweet post below into a 3–7 word title that we can insert as the title for the document that has this Linkedin post inside of it.

!IMPORTANT: Don’t respond with ANYTHING other than the completed 3–7 word title. That 3–7 word title should be the only thing in your response.

The tweet:

{{ $json.output }}
```

### 66. Set Post Content2
Data is normalized/transformed for the next step.

### 67. Code3
[Describe what this step does]

### 68. Extract Facebook IDs
Data is normalized/transformed for the next step.

## Output Schema
[Define expected output structure]

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Content Marketing Agency/Zoom Call _ Multi Content Copywriter + Scheduler.json`
Generated on: 2026-01-02
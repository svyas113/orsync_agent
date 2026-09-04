# Or-sync local sales agent

Local FastWorkflow sales and marketing agent for [Or-sync](https://orsync.co.in/). It answers customer questions, qualifies leads, books demos, and **never quotes prices** (human handoff instead).

Customers talk to this agent on WhatsApp, Instagram, ads, and the website. They are **not technical**. Keep every customer-facing reply simple.

---

## MUST CHANGE (next developer)

Do this before treating the agent as production-ready. These are product requirements, not optional polish.

### 1. Customer language — no framework internals

**Current problem:** replies can still drift into FastWorkflow / models / benchmarks.

**What customers should hear:** we built our own framework, so we can make **reliable agents at a lower cost**. That is the whole technical story.

**Change:** keep `orsync_workflow/application/orsync.py` and `_commands/` copy non-technical. If the LLM names FastWorkflow, Tau Bench, BERT, or similar, strip or rewrite it. Never walk a customer through how the stack works.

### 2. Strip markdown from customer replies

**Current problem:** WhatsApp / Instagram / ads should get plain text. Some LLM answers still return `**bold**`, headings, or lists.

**Change:** all customer output must go through `to_customer_text()` in `orsync_workflow/application/orsync.py`. Audit every command (`ask_orsync`, `request_demo`, `qualify_lead`, FastWorkflow clarification prompts). Remove remaining markdown, HTML (except the internal `<!-- HANDOFF:pricing -->` marker), and emoji-heavy formatting.

### 3. Dynamic pricing (required)

**Current behavior:** any price/cost/quote question escalates to a human (`escalate_pricing` → `data/handoffs.jsonl`). No numbers are quoted. That is intentional until pricing exists.

**Change:** build **dynamic pricing** so the agent can quote or estimate based on use case, channels, and integrations — then hand off only when the quote is out of policy or the customer asks to talk to a person. Do not invent prices in prompts until this system exists.

### 4. Route similar businesses to live demo agents

**Future product (not built yet):**

- Share the company website: https://orsync.co.in/
- When a customer describes a business similar to an agent we already shipped via **agent-builder**, send them the **link to that agent** so they can try it.
- Keep a catalog (industry / use case → public demo URL) and add a command such as `recommend_demo_agent`.

Until that catalog exists, do not invent demo URLs.

---

## Setup (local testing)

### Prerequisites

- Python 3.12 (this repo is pinned to `fastworkflow==2.22.3` and `dspy==3.2.1`)
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)
- Linux or WSL (Windows: use WSL)

Use `gemini/gemini-3.6-flash` for all LLM roles. Newer Gemini keys often cannot call `gemini-2.5-*`.

### Install

```bash
git clone https://github.com/svyas113/orsync_agent.git
cd orsync_agent
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp orsync_workflow/fastworkflow.passwords.env.example orsync_workflow/fastworkflow.passwords.env
```

Put the same Gemini key on every line in `orsync_workflow/fastworkflow.passwords.env`:

```
LITELLM_API_KEY_SYNDATA_GEN=your-key
LITELLM_API_KEY_PARAM_EXTRACTION=your-key
LITELLM_API_KEY_RESPONSE_GEN=your-key
LITELLM_API_KEY_PLANNER=your-key
LITELLM_API_KEY_AGENT=your-key
LITELLM_API_KEY_CONVERSATION_STORE=your-key
```

Never commit `fastworkflow.passwords.env`.

### Train (required once after clone, and again after command files change)

```bash
source .venv/bin/activate
fastworkflow train orsync_workflow orsync_workflow/fastworkflow.env orsync_workflow/fastworkflow.passwords.env
```

Takes several minutes on CPU. Writes `orsync_workflow/___command_info/` (gitignored).

### Run — inbox UI (recommended for testing)

On Windows, port 8080 is often used by other software (for example EDB Postgres). This app defaults to **8765**.

Terminal 1:

```bash
source .venv/bin/activate
python -m fastworkflow.run_fastapi_mcp \
  --workflow_path ./orsync_workflow \
  --env_file_path ./orsync_workflow/fastworkflow.env \
  --passwords_file_path ./orsync_workflow/fastworkflow.passwords.env \
  --host 127.0.0.1 \
  --port 8000
```

Terminal 2:

```bash
source .venv/bin/activate
INBOX_PORT=8765 python local_server.py
```

Open [http://127.0.0.1:8765](http://127.0.0.1:8765)

If 8765 is busy: `INBOX_PORT=8766 python local_server.py`

### Run — CLI

```bash
source .venv/bin/activate
fastworkflow run orsync_workflow orsync_workflow/fastworkflow.env orsync_workflow/fastworkflow.passwords.env
```

Try: `what do you do?`, `list your services`, `how much does it cost?`, `book a demo`.

Prefix with `/` for deterministic (non-agentic) mode, e.g. `/list services`.

---

## Project layout

```
orsync_workflow/
  application/orsync.py      # Company knowledge, leads, handoffs, plain-text helper
  _commands/                 # FastWorkflow command wrappers
  fastworkflow.env           # Model names (safe to commit)
  fastworkflow.passwords.env # API keys (do not commit)
chat_ui/                     # Local inbox (Web / WhatsApp / IG / Ads tabs)
local_server.py              # UI + proxy to FastWorkflow on :8000
data/                        # leads.jsonl, handoffs.jsonl (gitignored)
```

## Commands

| Command | Purpose |
|---------|---------|
| `list_services` | List offerings |
| `get_service_details` | One service |
| `explain_approach` | Why Or-sync / why cheaper (plain language) |
| `get_contact_info` | Email, website, response time |
| `qualify_lead` | Use case, industry, tools, timeline |
| `request_demo` | Book a demo |
| `escalate_pricing` | Human handoff for pricing |
| `ask_orsync` | Grounded Q&A |

## Channels (stubs)

Inbox tabs use `channel_id` values `web`, `whatsapp`, `instagram`, `ads`. Live WhatsApp / Instagram / Meta / Google ads adapters are not in this repo yet. They should call the same FastWorkflow `/invoke_agent_stream` endpoint.

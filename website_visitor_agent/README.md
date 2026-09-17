# Or-sync website visitor agent

FastWorkflow agent for [orsync.co.in](https://www.orsync.co.in): explains AI agents, answers brand questions, hands visitors public demo links (Spyran / Zebrata / RVD Jewels), and emails demo requests to **orsyncagents@gmail.com**.

## Layout

```
Or Sync Agent/
  orsync_visitor/           # FastWorkflow workflow
    application/            # session, brand copy, demos, SMTP emailer
    _commands/              # set_root_context + VisitorSession/*
    fastworkflow.env
    fastworkflow.passwords.env.example
    startup_action.json
    smoke_test.py
  run_orsync_visitor.sh     # starts FastAPI on 0.0.0.0:$PORT (default 8003)
  company_website/          # Vite/React site with embedded ChatWidget
```

Reuses the parent repo’s `fastapi_fastworkflow` package and `requirements.txt`.

## 1. Configure the agent

```bash
cd "/Users/srushtivaidya/Desktop/Orsync Dev"
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

cp "Or Sync Agent/orsync_visitor/fastworkflow.passwords.env.example" \
   "Or Sync Agent/orsync_visitor/fastworkflow.passwords.env"
```

Edit `fastworkflow.passwords.env`:

| Variable | Purpose |
|----------|---------|
| `LITELLM_API_KEY_*` / `GROQ_API_KEY` | LLM keys matching models in `fastworkflow.env` |
| `SMTP_USER` | Gmail address that sends mail (usually `orsyncagents@gmail.com`) |
| `SMTP_PASSWORD` | Gmail **App Password** (Google Account → Security → 2-Step Verification → App passwords) |
| `SMTP_FROM` | From address (defaults to `SMTP_USER`) |

Edit `orsync_visitor/fastworkflow.env` for public demo links:

| Variable | Purpose |
|----------|---------|
| `DEMO_SPYRAN_URL` | Public Spyran chat URL |
| `DEMO_ZEBRATA_URL` | Public Zebrata chat URL |
| `DEMO_RVD_URL` | Public RVD Jewels chat URL |
| `DEMO_REQUEST_TO` | Inbox for leads (default `orsyncagents@gmail.com`) |

If a demo URL is empty, the agent explains that demo and offers to request a private walkthrough instead.

## 2. Train intent models (first time / after command changes)

```bash
cd "/Users/srushtivaidya/Desktop/Orsync Dev"
.venv/bin/fastworkflow train \
  "./Or Sync Agent/orsync_visitor" \
  "./Or Sync Agent/orsync_visitor/fastworkflow.env" \
  "./Or Sync Agent/orsync_visitor/fastworkflow.passwords.env"
```

## 3. Run the agent API

```bash
cd "/Users/srushtivaidya/Desktop/Orsync Dev/Or Sync Agent"
./run_orsync_visitor.sh
# → http://localhost:8003  (Swagger at /docs)
```

On Render (or similar), set `PORT` and bind is already `0.0.0.0`. Add the same env/password values as service secrets.

## 4. Embed on the company website

`company_website/` is a working copy of [svyas113/company_website](https://github.com/svyas113/company_website) with a floating `ChatWidget`.

```bash
cd "Or Sync Agent/company_website"
cp .env.example .env
# set VITE_AGENT_API_URL to your agent host, e.g. http://localhost:8003
npm install
npm run dev
```

| Variable | Purpose |
|----------|---------|
| `VITE_AGENT_API_URL` | Agent FastAPI origin (no trailing slash). Used at **build** time by Vite. |

Production: set `VITE_AGENT_API_URL` to the deployed agent URL, rebuild (`npm run build`), redeploy the static site. Ensure the agent CORS allows `https://www.orsync.co.in` (current FastAPI stack allows `*`).

Push widget changes upstream to `svyas113/company_website` when ready.

## 5. Smoke test (no API keys)

```bash
cd "Or Sync Agent/orsync_visitor"
python3 smoke_test.py
```

## Visitor intents → commands

| Visitor ask | Command |
|-------------|---------|
| What can you do | `what_can_you_do` |
| What are AI agents / what do you do | `explain_ai_agents` |
| Company / brand | `about_orsync` |
| Services | `list_services` |
| Test agents / random demo | `open_demo_agent` |
| Request a demo | `request_demo` → email |

## Notes

- Demo handoff opens links in a new tab (widget linkifies `https://…` URLs).
- The site Contact form still only shows an alert; demo leads from the chat agent actually email the inbox when SMTP is configured.

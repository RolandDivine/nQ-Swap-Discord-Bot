# nQ-Swap Discord Bot

Production-focused Discord bot for crypto market pulse, trending tokens, new listings, and alerts.

## Enterprise production runbook

### 1) Install dependencies
```bash
python -m pip install -r requirements.txt
```

### 2) Configure environment
```bash
cp env.example .env
# edit .env values for DISCORD_TOKEN, CHANNEL_ID, GUILD_ID
```

### 3) Run preflight audit
```bash
python scripts/preflight_check.py
```

### 4) Run the bot
```bash
python scripts/run_bot.py
```

> This launcher validates dependencies and required environment variables before starting `bot.py`.

## Validation commands

```bash
python -m py_compile bot.py
python scripts/preflight_check.py
pytest -q
```

## Notes
- `requirements.txt` is the canonical dependency file for deployment tooling.
- Logs are written to `logs/nqswap.log` with rotation.

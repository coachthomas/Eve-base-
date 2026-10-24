# Eve 0.1 — local text chat (NOT DEPLOYED)

This is a real runnable, *local-only* prototype, not a mockup or a production service. It requires Python 3.11+, Ollama, and an Ollama-compatible locally installed chat model. **No model weights or hosted service are included.** Model choice/identifier must be checked against the installed Ollama models (`ollama list`); the default `granite4:micro` is a configuration candidate, not a verified installed model.

## Run on a machine with adequate resources

1. Install Ollama from its official website, and download an appropriately licensed model. Verify license and hardware first.
2. Start the Ollama local service. Use `ollama list` to find your actual model name.
3. From this repository root, launch: `EVE_MODEL=<installed-model-name> python3 apps/eve-chat/server.py`
4. On **that same machine**, open http://127.0.0.1:8765 and send a message.
5. Exit with Ctrl-C. Relaunch to confirm conversations persist in local SQLite.

The server listens ONLY on 127.0.0.1 and has NO authentication, so it is intentionally inaccessible to a remote iPad. To use from an iPad we must design a properly authenticated remote access path first. Do not change the bind address to 0.0.0.0 or put this server behind a public reverse proxy without authentication, TLS, CSRF protection, logging controls, isolation, and a security review.

## Boundaries

- Constitution is loaded from `docs/constitution.md` on each reply.
- Only successful exchanges are recorded in the local SQLite database `apps/eve-chat/private/eve.sqlite3` (or `EVE_DB_PATH`). Never commit the database to this public repository.
- Prior messages are included as limited context, NOT extracted durable memories or online training.
- Model generation isn't guaranteed truthful or constitution-compliant.
- No autonomous work, code modification, internet research, user logins, voice, payments, direct ChatGPT integration, or deployed domain exists here.
- The code has not been executed on a model host by this GitHub commit. First verified run and functional tests remain outstanding.
- The database directory should stay out of version control: do not `git add -f` personal data.

## Next acceptance test

Run locally, send "Hello Eve", close/reopen page, verify conversation history. Restart server and verify the same persisted messages. Verify a missing Ollama service returns an explicit failure instead of fictitious success. Then add authentication before remote use.

Target future address (not live): `eve.energyculture.org`.

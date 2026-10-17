# Energy Culture continuous worker

A restartable implementation worker, not a claim that the commercial Lead Runner is operational. It resumes a SQLite job queue, performs bounded OpenAI Responses API code steps, writes authorized source files, runs existing collector tests, rolls back failed steps, and continues until a job is locally complete or blocked. Python 3.11+; no installed packages required.

## Current deployment state
Built and tested in a temporary workspace. API key created in Personal / Default project and saved only in the operator-confirmed `.env.local` outside this repository. Authentication tested using the models endpoint; no generated API response was purchased. No permanent server has been selected or provisioned. No system service is installed. No API secret is in GitHub. This is NOT yet an unattended live deployment.

## Operator installation on a persistent Linux host
1. Use an existing Linux host with outbound HTTPS to api.openai.com and a durable disk. Running this in a transient ChatGPT workspace is insufficient.
2. Create a dedicated unprivileged `ecworker` service account. Place this repository at `/opt/energy-culture`. Keep worker source and configuration root-owned, and create `/opt/energy-culture/docs/lead-runner`. Give ecworker write access only to the two source directories listed in the unit plus its state directory.
3. Create `/etc/energy-culture-worker.env` as root, mode 0600, using `deploy/environment.example`; transfer the secret securely from its confirmed location. Approve a daily call allowance and configure it. Default 0 makes no billable model calls. Call cap is not a dollar cap; use project billing controls as well. An authenticated key does not prove funded API access.
4. Install `deploy/energy-culture-worker.service` into `/etc/systemd/system/`, then run `systemctl daemon-reload` and `systemctl enable --now energy-culture-worker`. Restart on failure and startup after host reboot are handled by systemd.
5. As ecworker, enqueue the supplied job with `python3 /opt/energy-culture/ops/continuous-worker/worker.py enqueue --id lead-runner-build-1 --prompt-file /opt/energy-culture/ops/continuous-worker/lead-runner-job.md`. Inspect `status` and `journalctl -u energy-culture-worker`.

## Operation and verification
Use `status` for last heartbeat and job state. `pause` stops new steps; an in-flight call may finish. `unpause` allows new steps. `resume --id JOB` retries a blocked job after the dependency is fixed; it does not reset lifetime round counts. Stop the service to halt the process. Zero queued jobs means idle, not failed and not continued progress. A stale heartbeat indicates the host/worker needs attention; no external alert service has been connected.

Single process lock prevents overlap. Interrupted jobs requeue on restart; pending writes roll back before resuming. API calls are reserved before dispatch so crashes and retries count toward the daily UTC allowance. Lost API responses may still be billed; a restart may repeat the reasoning step. Retry failures three times with backoff, then record a blocker. Queue, checkpoints and event journal remain private on durable disk. Back up the state directory while the service is stopped.

The model can edit only apps/lead-discovery/ and docs/lead-runner/. It cannot edit its own policy, access credentials through model tools, publish, contact people or spend outside model calls. Checks execute repository Python code under the dedicated account, with a minimal environment and without the API key. This is process isolation and service hardening, not a complete hostile-code sandbox; use a dedicated host/container without unrelated secrets. The model can change tests: passing tests alone is not proof of commercial readiness. A successful job means locally verified changes only. Existing Wix source and live service credentials are NOT automatically available from ChatGPT connectors; they require a separate host integration.

## Tests
`python3 -m unittest discover -s ops/continuous-worker/tests -v`
`PYTHONPATH=apps/lead-discovery python3 -m unittest discover -s apps/lead-discovery/tests -v`

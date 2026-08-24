# Scheduling the standing loop

The engine holds no daemon: cadence is delivered by the environment
(RFC 0019, D-19.1). Two equivalent ways to deliver it.

**systemd user timer** (preferred on this machine): adjust the paths in
`torve-tick.service` — the engine checkout with its `.env`, and a
*stable* clone of this repository (not a scratchpad path) — then:

    cp ops/torve-tick.* ~/.config/systemd/user/
    systemctl --user daemon-reload
    systemctl --user enable --now torve-tick.timer

**cron**, one line, same shape:

    */10 * * * * cd $HOME/GitLibrary/Morze/torve && sh -c 'set -a; . ./.env; set +a; uv run torve tick --root $HOME/torve-remote-lab' >> $HOME/.local/state/torve-tick.log 2>&1

Overlap is safe either way: a tick that finds the lock held exits as a
recorded no-op. Turning the loop off is unscheduling it — there is no
enabled flag. Watch it through the telemetry: every tick appends one
`tick` engine event; honest noops are the heartbeat, silence means the
scheduler is dead, a repeating pause reason means the escalation queue
wants you.

# The durable run store

Real runs take a postgres store (RFC 0003, D-3.6); this lab's is a
local container with a named volume, so the run records survive both
the container and the machine's reboots:

    docker volume create torve-lab-pg-data
    docker run -d --name torve-lab-pg --restart unless-stopped \
      -e POSTGRES_PASSWORD=<generate one> \
      -e POSTGRES_USER=torve -e POSTGRES_DB=torve_lab \
      -v torve-lab-pg-data:/var/lib/postgresql/data \
      -p 127.0.0.1:15433:5432 postgres:16-alpine

The DSN lives only in the engine checkout's `.env` as `TORVE_PG_DSN`
(`postgresql://torve:<password>@127.0.0.1:15433/torve_lab`) — the
config here names the variable, never the value. First-time setup and
every forze upgrade end the same way:

    torve migrate --all --root <this repo>
    torve doctor --root <this repo>

`torve doctor` is the whole preflight: it reds with an instruction when
the DSN is unset, the database does not answer, or a substrate step is
pending.

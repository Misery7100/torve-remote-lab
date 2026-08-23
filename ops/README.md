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

    */30 * * * * cd $HOME/GitLibrary/Morze/torve && sh -c 'set -a; . ./.env; set +a; uv run torve tick --root $HOME/torve-remote-lab' >> $HOME/.local/state/torve-tick.log 2>&1

Overlap is safe either way: a tick that finds the lock held exits as a
recorded no-op. Turning the loop off is unscheduling it — there is no
enabled flag. Watch it through the telemetry: every tick appends one
`tick` engine event; honest noops are the heartbeat, silence means the
scheduler is dead, a repeating pause reason means the escalation queue
wants you.

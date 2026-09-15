#!/bin/bash
set -euo pipefail

# Accept RUN_TIME or run_time (HH:MM, 24-hour). Optional TZ for the container clock.
SCHEDULE_TIME="${RUN_TIME:-${run_time:-}}"

seconds_until() {
    local target_hm="$1"
    local now target
    now=$(date +%s)
    # GNU date (Ubuntu): next occurrence of today's HH:MM, or tomorrow if already past.
    target=$(date -d "today ${target_hm}" +%s)
    if [ "$now" -ge "$target" ]; then
        target=$(date -d "tomorrow ${target_hm}" +%s)
    fi
    echo $((target - now))
}

if [ -n "$SCHEDULE_TIME" ]; then
    if ! [[ "$SCHEDULE_TIME" =~ ^([01]?[0-9]|2[0-3]):[0-5][0-9]$ ]]; then
        echo "Invalid RUN_TIME '${SCHEDULE_TIME}'. Use 24-hour HH:MM (e.g. 06:00)." >&2
        exit 1
    fi

    echo "Scheduler enabled: deemon refresh daily at ${SCHEDULE_TIME} (TZ=${TZ:-UTC})"
    while true; do
        wait_secs=$(seconds_until "$SCHEDULE_TIME")
        next_at=$(date -d "+${wait_secs} seconds" '+%Y-%m-%d %H:%M %Z')
        echo "Next refresh at ${next_at} (sleeping ${wait_secs}s)"
        sleep "$wait_secs"
        echo "Running: deemon refresh"
        deemon refresh || echo "Refresh exited with status $? — will retry at next RUN_TIME" >&2
    done
fi

exec deemon "$@"

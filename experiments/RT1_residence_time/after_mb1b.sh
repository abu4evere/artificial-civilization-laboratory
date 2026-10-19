#!/bin/sh
# Starts RT1b (frozen as RT1b-frozen) once MB1b reports ALL DONE. Refuses if an RT1b run is already going.
cd /d/acl/experiments
until grep -q "ALL DONE" MB1_multi_band/run_mb1b.log 2>/dev/null; do sleep 300; done
if pgrep -f "run_rt1b.py run" >/dev/null 2>&1 || pgrep -f "run_rt1b.py one" >/dev/null 2>&1; then exit 0; fi
cd RT1_residence_time && python run_rt1b.py run > run_rt1b.log 2>&1

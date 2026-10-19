#!/bin/sh
# Starts FX2 (frozen as FX2-frozen) once RT1b reports ALL DONE.
cd /d/acl/experiments
until grep -q "ALL DONE" RT1_residence_time/run_rt1b.log 2>/dev/null; do sleep 300; done
cd FX2_embedded_food && python run_fx2.py run > run_fx2.log 2>&1

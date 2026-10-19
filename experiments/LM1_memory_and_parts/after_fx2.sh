#!/bin/sh
# Starts LM1 (frozen as LM1-frozen) once FX2 reports ALL DONE and Amendment 1 is approved by the creator.
cd /d/acl/experiments
until grep -q "ALL DONE" FX2_embedded_food/run_fx2.log 2>/dev/null && grep -q "Amendment 1 status: APPROVED" LM1_memory_and_parts/proposal.md; do sleep 600; done
cd LM1_memory_and_parts && python run_lm1.py run > run_lm1.log 2>&1

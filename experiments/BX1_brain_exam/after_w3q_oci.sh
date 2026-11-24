#!/bin/bash
# BX1, once W3q has finished on this machine: (1) old mind on school lives 201-300, 4 workers x 25;
# (2) the after-school test on new worlds 20001-20150: OLD, MBB, SCHOOL, 3 workers x 50 each (questions.md addendum).
cd ~/bx1
PY=/home/ubuntu/venv/bin/python
while pgrep -f "bin/python w3q[.]py run" >/dev/null; do sleep 300; done
for k in 0 1 2 3; do
  BX1_BASELINE=1 BX1_START=$((200+25*k)) BX1_PART=_oci$k OMP_NUM_THREADS=1 nohup $PY run_school.py 25 > base_$k.out 2>&1 &
done
for k in 0 1 2; do
  BX1_BASELINE=1 BX1_SEED0=20001 BX1_START=$((50*k)) BX1_PART=_test$k OMP_NUM_THREADS=1 nohup $PY run_school.py 50 > test_old_$k.out 2>&1 &
  BX1_FIXED=mbb_seed1.npz BX1_SEED0=20001 BX1_START=$((50*k)) BX1_PART=_test$k OMP_NUM_THREADS=1 nohup $PY run_school.py 50 > test_mbb_$k.out 2>&1 &
  BX1_FIXED=school_brain_300.npz BX1_SEED0=20001 BX1_START=$((50*k)) BX1_PART=_test$k OMP_NUM_THREADS=1 nohup $PY run_school.py 50 > test_school_$k.out 2>&1 &
done
echo "$(date "+%F %H:%M") started 4 baseline workers and 9 test workers" >> after.log

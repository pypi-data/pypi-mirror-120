#!/bin/bash

CMD="$@"

COUNT=5
AFFINITY="taskset --cpu-list 5"
TIME_FORMAT='Wall: %e
System: %S
User: %U
Major Faults: %F
Minor Faults: %R
FileSystem Inputs: %I
FileSystem Outputs: %O
Max Mem: %Mk
Swapped Out: %W
Context switched (forced): %c
Context switched (voluntary): %w
Signaled (unix): %k
Received socket messages: %r
Sent socket messages: %s
'

for i in `seq $COUNT`; do
    echo "======================================"
    echo "Benchmark: ${i} - $CMD"
    echo "======================================"
    $AFFINTY /usr/bin/time -f "$TIME_FORMAT" -- $CMD >/dev/null
done

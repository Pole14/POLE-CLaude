#!/bin/bash
n=$1; cd "$(dirname "$0")"; E=/home/claude/pole-claude/engine
SONG=$(python3 -c "import json;print(json.load(open('${n}_base.json'))['song'])")
python3 $E/explainer.py $n.json $n.mp4 >/dev/null 2>$n.err && python3 $E/mux3.py $n.mp4 ${n}_base.json out_$n.mp4 /home/claude/pole-claude/music/$SONG.mp3 0 -22 >/dev/null 2>>$n.err && echo done $n || echo FAIL $n

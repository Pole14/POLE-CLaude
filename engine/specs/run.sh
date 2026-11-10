#!/bin/bash
# run.sh ID -> render + mezcla en g13/out_ID.mp4
n=$1; cd /tmp/claude-0/-home-claude/5c0c8665-fdf5-5301-970e-bfb2f9a212f4/scratchpad/g13
E=/home/claude/pole-claude/engine
REC=$(python3 -c "import json;print(json.load(open('${n}_base.json'))['rec'])"); SONG=$(python3 -c "import json;print(json.load(open('${n}_base.json'))['song'])")
python3 $E/hero.py $REC $n.json $n.mp4 >/dev/null 2>$n.err && python3 $E/mux3.py $n.mp4 ${n}_base.json out_$n.mp4 /home/claude/pole-claude/music/$SONG.mp3 0 >/dev/null 2>>$n.err && echo done $n || echo FAIL $n

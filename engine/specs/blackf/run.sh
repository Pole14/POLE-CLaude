#!/bin/bash
n=$1; cd /tmp/claude-0/-home-claude/5c0c8665-fdf5-5301-970e-bfb2f9a212f4/scratchpad/bf
E=/home/claude/pole-claude/engine
REC=$(python3 -c "import json;print(json.load(open('${n}_base.json'))['rec'])"); SONG=$(python3 -c "import json;print(json.load(open('${n}_base.json'))['song'])")
LU=-28; case $n in F*) LU=-23;; esac
python3 $E/hero.py $REC $n.json $n.mp4 >/dev/null 2>$n.err && python3 $E/mux3.py $n.mp4 ${n}_base.json out_$n.mp4 /home/claude/pole-claude/music/$SONG.mp3 0 $LU >/dev/null 2>>$n.err && echo done $n || echo FAIL $n

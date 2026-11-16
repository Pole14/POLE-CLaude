#!/bin/bash
# run.sh ID -> render con dopa.py y mezcla SOLO VOZ a -15 LUFS (sin música)
n=$1; cd "$(dirname "$0")"; E=/home/claude/pole-claude/engine
python3 $E/dopa.py $n.json $n.mp4 >/dev/null 2>$n.err && ffmpeg -v error -y -i $n.mp4 -i /home/claude/pole-claude/voices/dp_$n.wav -filter_complex "[1:a]loudnorm=I=-15:TP=-1.5:LRA=11,apad[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest out_$n.mp4 2>>$n.err && echo done $n || echo FAIL $n

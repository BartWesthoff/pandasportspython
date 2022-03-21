#!/bin/bash
let c=0
for i in `cat squats.txt`; do	
	youtube-dl $i -o ./output/$c
	let c++
done
wait

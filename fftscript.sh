#!/bin/bash
arecord -D plughw:0 --duration=5 --channels=1 --rate=44100 output.wav

python testfft.py

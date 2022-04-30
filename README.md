# impro_with_algo
A setup to improvise over chords where algorithm and human alternately play and inspire each other.

## Basic Concept
Sonic Pi is used to play out beat and chords.
It does the synchronization automatically.
Via an OSC server Sonic Pi can request and receive music from a python scrip.
The python script calls an algorithm to compose the music.
This composing script can be written in python also and could be interactive.
That means it could listen to the human and adapting the music accordingly.
Or it could use face recognition an a camera to match the mood of a human...

## Current state
- Sonic Pi <> Python communication works
- Phrase consists of 4 bars of a C7 chord
- Python 'composes' dummy phrase for every second phrase

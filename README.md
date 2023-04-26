# Midi to NFA Visualizer

This project was completed as an Honors Contract/Extra Credit Project for CSE 355 (Introduction to Theoretical Computer Science).

Demonstration Video: https://youtu.be/Ye_T-lA8hKQ

hi so I know practically nothing about music theory, so mb if this is inaccurate in a bunch of ways lol

an issue I came across was finding the correct rate to run the program at:
- pygame uses clock.tick(#) to set framerate and run the main game loop at a specified rate (I store this framerate value in a variable called FPS)
- each midi file is made up of messages (notes to play) and meta information, which includes things like tempo and ticks_per_beat (and time signature but idk what to do with that)
- the array holding all of the values for the notes has an entry for every single tick (if you look at the output of the mido object, each 'message' plays a note for a certain 'time' value, which corresponds to number of ticks to wait until playing the note; i.e. previous note played for next note's time value)
- I think the problem is that my computer can't handle an FPS of ticks_per_beat (often something like 480) so it lags and then the songs slow down
- so the solution was to essentially "downsample," and remove some of the ticks (depending on the DOWNSAMPLE_RATE variable)
- i still can't calculate FPS correctly though because I have absolutely no idea how time signature works or if it's even relevant and I also dunno how to calculate it using tempo and ticks_per_beat lol oh whale

## References
### Libraries
- PyGame: https://www.pygame.org/docs/
- PyFluidSynth: https://github.com/nwhitehead/pyfluidsynth
- Mido: https://mido.readthedocs.io/en/latest/

### Downloads/Resources
- Piano SoundFont file (I used the "Steinway B" one): https://musical-artifacts.com/artifacts?formats=sf2&tags=piano
- Twinkle Twinkle Little Star: https://bitmidi.com/twinkle-twinkle-little-star-mid
- Fur Elise: http://www.piano-midi.de/beeth.htm
- Mario theme (in description of video): https://www.youtube.com/watch?v=qEjbJG4tjGY
- shhh: https://www.youtube.com/watch?v=8xwzbeMD9Ds

### Helpful Articles and Videos
- Convert MIDI to NumPy Array Article: https://medium.com/analytics-vidhya/convert-midi-file-to-numpy-array-in-python-7d00531890c
- Chart for MIDI to piano notes (also in the article): https://miro.medium.com/v2/resize:fit:640/1*SPjkKvreiBauJA3Lzvy8FQ.gif
- Visualization of NumPy operations: https://www.youtube.com/watch?v=XC_j0cr_a8U

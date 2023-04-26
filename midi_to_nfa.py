import pygame
from pygame.locals import *
import math
import mido
import numpy as np
import string
import fluidsynth

# initialize PyGame
pygame.init()

# constants (don't change)
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 720
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("CSE 355 Honors Project")
COLOR_BACKGROUND = (225, 225, 225)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
CIRCLE_RADIUS = 25
FONT = pygame.font.SysFont(None, 30)

# audio stuff (fluidsynth): https://github.com/nwhitehead/pyfluidsynth
TRACK = 0
fs = fluidsynth.Synth()
sfid = fs.sfload("Grotrian_Concert_Royal.sf2") # https://musical-artifacts.com/artifacts?formats=sf2&tags=piano

# songs (midi files parsed using mido): https://mido.readthedocs.io/en/latest/
song1 = mido.MidiFile('./Songs/twinkle-twinkle-little-star.mid', clip=True) # https://bitmidi.com/twinkle-twinkle-little-star-mid
song2 = mido.MidiFile('./Songs/elise.mid', clip=True) # http://www.piano-midi.de/beeth.htm
song3 = mido.MidiFile('./Songs/mario.mid', clip=True) # https://www.youtube.com/watch?v=qEjbJG4tjGY
rick = mido.MidiFile('./Songs/rick.mid', clip=True) # https://www.youtube.com/watch?v=8xwzbeMD9Ds

# SETTINGS (change these to get it to play correctly)
SONG = rick # CHANGE THIS TO SELECT SONG (from above list)
USE_CALCULATED_RATES = False # i am bad at math so probably don't use this lmao (mess around with DOWNSAMPLE_RATE if you do use this)
FPS = SONG.ticks_per_beat * 2 # how often the main loop runs; if FPS = 60, then 60 times per second
DOWNSAMPLE_RATE = 2 # reduce number of values in the results_array (values / DOWNSAMPLE_RATE) because otherwise program dies lol (reduces quality but it's ok)
CONSOLE_OUTPUT = False # CHANGE THIS TO OUTPUT THE STATE OF THE NFA IN EACH ITERATION
SHOW_NOTES = True # CHANGE THIS TO SHOW PIANO NOTES INSTEAD OF q# STATES
TURN_OFF_Q0 = False # this makes it technically not an NFA but I like it more with this b/c its like q0 is silent state
ADD_BREAKS = True # for songs that don't have breaks between repeat notes, add them (not really a solution; this causes offset - the higher DOWNSAMPLE_RATE is, the more noticeable it is)

# hard coding for showcase (lmao)
if SONG is song1:
    FPS = 240
    DOWNSAMPLE_RATE = 3
    ADD_BREAKS = False
elif SONG is song2:
    FPS = 240
    DOWNSAMPLE_RATE = 3
elif SONG is song3:
    FPS = 200
    DOWNSAMPLE_RATE = 8
elif SONG is rick:
    FPS = 120
    DOWNSAMPLE_RATE = 1.8

# list to hold NFA states and info about them
# each state has:
# active (True/False): updates color of circle
# position: center of circle (positions of q1 thru q88 calculated at beginning of main)
# label: name of state
# note: MIDI note (piano note) from 21-108
nfa = [
    {'active': True, 'position': (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 'label': "q0", 'note': -1, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q1", 'note':21, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q2", 'note':22, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q3", 'note':23, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q4", 'note':24, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q5", 'note':25, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q6", 'note':26, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q7", 'note':27, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q8", 'note':28, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q9", 'note':29, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q10", 'note':30, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q11", 'note':31, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q12", 'note':32, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q13", 'note':33, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q14", 'note':34, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q15", 'note':35, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q16", 'note':36, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q17", 'note':37, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q18", 'note':38, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q19", 'note':39, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q20", 'note':40, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q21", 'note':41, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q22", 'note':42, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q23", 'note':43, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q24", 'note':44, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q25", 'note':45, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q26", 'note':46, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q27", 'note':47, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q28", 'note':48, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q29", 'note':49, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q30", 'note':50, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q31", 'note':51, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q32", 'note':52, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q33", 'note':53, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q34", 'note':54, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q35", 'note':55, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q36", 'note':56, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q37", 'note':57, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q38", 'note':58, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q39", 'note':59, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q40", 'note':60, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q41", 'note':61, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q42", 'note':62, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q43", 'note':63, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q44", 'note':64, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q45", 'note':65, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q46", 'note':66, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q47", 'note':67, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q48", 'note':68, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q49", 'note':69, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q50", 'note':70, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q51", 'note':71, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q52", 'note':72, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q53", 'note':73, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q54", 'note':74, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q55", 'note':75, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q56", 'note':76, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q57", 'note':77, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q58", 'note':78, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q59", 'note':79, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q60", 'note':80, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q61", 'note':81, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q62", 'note':82, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q63", 'note':83, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q64", 'note':84, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q65", 'note':85, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q66", 'note':86, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q67", 'note':87, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q68", 'note':88, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q69", 'note':89, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q70", 'note':90, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q71", 'note':91, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q72", 'note':92, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q73", 'note':93, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q74", 'note':94, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q75", 'note':95, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q76", 'note':96, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q77", 'note':97, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q78", 'note':98, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q79", 'note':99, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q80", 'note':100, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q81", 'note':101, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q82", 'note':102, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q83", 'note':103, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q84", 'note':104, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q85", 'note':105, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q86", 'note':106, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q87", 'note':107, 'velocity':0},
    {'active': False, 'position': (0, 0), 'label': "q88", 'note':108, 'velocity':0}
]

def main():
    # calculate the positions of each state (yes I know this is scuffed but oh well)
    for i in range(88):
        # calculate the angle for the current circle
        if i+1 <= 11:
            angle = i * 2 * math.pi / 11
        elif i+1 <= 29:
            angle = i * 2 * math.pi / 18
        elif i+1 <= 53:
            angle = i * 2 * math.pi / 24
        else:
            angle = i * 2 * math.pi / 35
        
        # calculate the x and y coordinates for the current circle
        if i+1 <= 11:
            offset_factor = 4
        elif i+1 <= 29:
            offset_factor = 6.5
        elif i+1 <= 53:
            offset_factor = 9
        else:
            offset_factor = 11.5
        x = (WINDOW_WIDTH / 2) + CIRCLE_RADIUS * offset_factor * math.cos(angle)
        y = (WINDOW_HEIGHT / 2) + CIRCLE_RADIUS * offset_factor * math.sin(angle)
        
        # update the array
        nfa[i+1]['position'] = (int(x), int(y))
    
    # convert MIDI file into array of note states at each time interval
    result_array = convert_midi(SONG)
    counter = 0
    
    # initialize fluidsynth
    fs.start()
    fs.program_select(TRACK, sfid, 0, 0)
    
    # control FPS using clock
    clock = pygame.time.Clock()
    
    # determine proper FPS and downsampling rate to use for song to play at correct pace
    if USE_CALCULATED_RATES:
        calculate_rates(len(result_array))
    
    # update labels depending on SHOW_NOTES setting
    change_labels()
    
    if CONSOLE_OUTPUT: 
        print("playing song...")
    
    # Game loop
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                break
        
        # music logic (only update music if there are still rows in array)
        if (counter < len(result_array)):
            update_states(result_array[counter])
            play_sound()
            counter += 1
            if CONSOLE_OUTPUT:
                print("\nIteration:", counter)
        else:
            # end of song go back to default
            for state in nfa:
                if state != nfa[0]:
                    state['active'] = False
            if counter == len(result_array):
                if CONSOLE_OUTPUT:
                    print("finished playing song.")
        
        # continuously update screen
        draw_window()

# call every game loop
def draw_window():
    WINDOW.fill(COLOR_BACKGROUND)
    draw_arrows()
    draw_states()
    pygame.display.update()

# function to draw states based on their values in the nfa list
def draw_states():
    for state in nfa:
        pygame.draw.circle(
            WINDOW,
            COLOR_GREEN if state['active'] else COLOR_RED,
            state['position'],
            CIRCLE_RADIUS
        )
        label = FONT.render(state['label'], True, COLOR_BLACK)
        label_rect = label.get_rect()
        label_rect.center = state['position']
        WINDOW.blit(label, label_rect)

# draws connections between states (just lines because idk)
# yes I know my drawing isn't truthfully a proper NFA but I'm not going to draw more lines because I'm lazy, sorry
def draw_arrows():
    for state in nfa:
        pygame.draw.line(WINDOW, COLOR_BLACK, state['position'], nfa[0]['position'], 2)

# updates the active values of the states (draw_states will update them accordingly)
def update_states(current_status):
    q0_state = True
    # go through each node and update 'active' depending on current_status value
    for i in range(len(current_status)):
        # update note at index i+1 in the big array (q1-q88)
        nfa[i+1]['velocity'] = current_status[i]
        # this is for q0 (no sound being played)
        if nfa[i+1]['active'] == True:
            q0_state = False if TURN_OFF_Q0 == True else True
            if CONSOLE_OUTPUT:
                print("note", i+1, "- Active")
    nfa[0]['active'] = q0_state

# plays sound depending on state value in nfa
def play_sound():
    for state in nfa:
        if state['velocity'] != 0:
            if state['active'] != True: # ONLY PLAY NOTE IF NOT ALREADY ACTIVE (otherwise it plays every single tick, which tbf is kinda funny)
                state['active'] = True
                fs.noteon(TRACK, state['note'], state['velocity'])
        else:
            if state is not nfa[0]: # don't change q0
                state['active'] = False
                fs.noteoff(TRACK, state['note'])

# determines proper FPS to use for song to play at correct pace
def calculate_rates(total_ticks): # pass in total number of ticks from generated array
    ticks_per_beat = SONG.ticks_per_beat
    tempo = 500000 # microseconds per beat; 500000 is default (= 120 bpm)
    for msg in SONG.tracks[0]:
        if msg.type == 'set_tempo':
            tempo = msg.tempo
    # i have no idea how to properly calculate this but oh whale
    # total_beats = total_ticks / ticks_per_beat
    seconds_per_beat = tempo / 1000000
    beats_per_second = 1 / seconds_per_beat
    # seconds = (total_beats / seconds_per_beat)
    FPS = (ticks_per_beat * beats_per_second) / DOWNSAMPLE_RATE # ticks per second and adjust based on DOWNSAMPLE_RATE
    print("ticks_per_beat:", ticks_per_beat, "- tempo:", tempo)
    print("FPS:", FPS, "- DOWNSAMPLE_RATE:", DOWNSAMPLE_RATE)
    # print("seconds:", seconds)

# https://miro.medium.com/v2/resize:fit:640/1*SPjkKvreiBauJA3Lzvy8FQ.gif
def change_labels():
    if SHOW_NOTES == True:
        for state in nfa:
            match state['label']:
                case 'q1': state['label'] = 'A0'
                case 'q2': state['label'] = 'Bb0'
                case 'q3': state['label'] = 'B0'
                case 'q4': state['label'] = 'C1'
                case 'q5': state['label'] = 'Db1'
                case 'q6': state['label'] = 'D1'
                case 'q7': state['label'] = 'Eb1'
                case 'q8': state['label'] = 'E1'
                case 'q9': state['label'] = 'F1'
                case 'q10': state['label'] = 'Gb1'
                case 'q11': state['label'] = 'G1'
                case 'q12': state['label'] = 'Ab1'
                case 'q13': state['label'] = 'A1'
                case 'q14': state['label'] = 'Bb1'
                case 'q15': state['label'] = 'B1'
                case 'q16': state['label'] = 'C2'
                case 'q17': state['label'] = 'Db2'
                case 'q18': state['label'] = 'D2'
                case 'q19': state['label'] = 'Eb2'
                case 'q20': state['label'] = 'E2'
                case 'q21': state['label'] = 'F2'
                case 'q22': state['label'] = 'Gb2'
                case 'q23': state['label'] = 'G2'
                case 'q24': state['label'] = 'Ab2'
                case 'q25': state['label'] = 'A2'
                case 'q26': state['label'] = 'Bb2'
                case 'q27': state['label'] = 'B2'
                case 'q28': state['label'] = 'C3'
                case 'q29': state['label'] = 'Db3'
                case 'q30': state['label'] = 'D3'
                case 'q31': state['label'] = 'Eb3'
                case 'q32': state['label'] = 'E3'
                case 'q33': state['label'] = 'F3'
                case 'q34': state['label'] = 'Gb3'
                case 'q35': state['label'] = 'G3'
                case 'q36': state['label'] = 'Ab3'
                case 'q37': state['label'] = 'A3'
                case 'q38': state['label'] = 'Bb3'
                case 'q39': state['label'] = 'B3'
                case 'q40': state['label'] = 'C4'
                case 'q41': state['label'] = 'Db4'
                case 'q42': state['label'] = 'D4'
                case 'q43': state['label'] = 'Eb4'
                case 'q44': state['label'] = 'E4'
                case 'q45': state['label'] = 'F4'
                case 'q46': state['label'] = 'Gb4'
                case 'q47': state['label'] = 'G4'
                case 'q48': state['label'] = 'Ab4'
                case 'q49': state['label'] = 'A4'
                case 'q50': state['label'] = 'Bb4'
                case 'q51': state['label'] = 'B4'
                case 'q52': state['label'] = 'C5'
                case 'q53': state['label'] = 'Db5'
                case 'q54': state['label'] = 'D5'
                case 'q55': state['label'] = 'Eb5'
                case 'q56': state['label'] = 'E5'
                case 'q57': state['label'] = 'F5'
                case 'q58': state['label'] = 'Gb5'
                case 'q59': state['label'] = 'G5'
                case 'q60': state['label'] = 'Ab5'
                case 'q61': state['label'] = 'A5'
                case 'q62': state['label'] = 'Bb5'
                case 'q63': state['label'] = 'B5'
                case 'q64': state['label'] = 'C6'
                case 'q65': state['label'] = 'Db6'
                case 'q66': state['label'] = 'D6'
                case 'q67': state['label'] = 'Eb6'
                case 'q68': state['label'] = 'E6'
                case 'q69': state['label'] = 'F6'
                case 'q70': state['label'] = 'Gb6'
                case 'q71': state['label'] = 'G6'
                case 'q72': state['label'] = 'Ab6'
                case 'q73': state['label'] = 'A6'
                case 'q74': state['label'] = 'Bb6'
                case 'q75': state['label'] = 'B6'
                case 'q76': state['label'] = 'C7'
                case 'q77': state['label'] = 'Db7'
                case 'q78': state['label'] = 'D7'
                case 'q79': state['label'] = 'Eb7'
                case 'q70': state['label'] = 'E7'
                case 'q81': state['label'] = 'F7'
                case 'q82': state['label'] = 'Gb7'
                case 'q83': state['label'] = 'G7'
                case 'q84': state['label'] = 'Ab7'
                case 'q85': state['label'] = 'A7'
                case 'q86': state['label'] = 'Bb7'
                case 'q87': state['label'] = 'B7'
                case 'q88': state['label'] = 'C8'

###################################
# below code converts midi to array; each array entry is one tick; for tempo of 500000 microseconds (120 BPM), 
# reference: https://medium.com/analytics-vidhya/convert-midi-file-to-numpy-array-in-python-7d00531890c
###################################
# parses each message in the midi and returns dictionary of important values:
# time, note, velocity, on_status
def parse_message(msg):
    result = dict() 
    if 'note_on' in msg:
        result['on_status'] = True
    elif 'note_off' in msg:
        result['on_status'] = False
    else:
        result['on_status'] = None
    
    # get 'time' value from msg 
    result['time'] = int(msg[msg.rfind('time'):].split(' ')[0].split('=')[1].translate(
        str.maketrans({a: None for a in string.punctuation})))
    
    # also get 'note' and 'velocity' if msg shows note as on
    if result['on_status'] is not None:
        result['note'] = int(msg[msg.rfind('note'):].split(' ')[0].split('=')[1].translate(
            str.maketrans({a: None for a in string.punctuation})))
        result['velocity'] = int(msg[msg.rfind('velocity'):].split(' ')[0].split('=')[1].translate(
            str.maketrans({a: None for a in string.punctuation})))
    # return dictionary with: time, note, velocity, on_status
    return result

# updates the state of each note (each of the 88 values)
def update_note(last_state, note, velocity, on_status=True):
    result = [0] * 88 if last_state is None else last_state.copy() # go based off of last_state & make modifications
    if 21 <= note <= 108: # midi piano note format; ranges from 21 to 108
        result[note-21] = velocity if on_status else 0 # update specified note 
    return result # return an array of 88 values (note states)

# get the new state based on the next message
def get_new_state(new_msg, last_state):
    new_msg = parse_message(str(new_msg)) # format the message (passed in as whatever format) into dict of important values
    new_state = update_note(last_state, note=new_msg['note'], velocity=new_msg['velocity'], on_status=new_msg['on_status']) if new_msg['on_status'] is not None else last_state
    return [new_state, new_msg['time']]

# convert track to python data structure (2d list)
def convert_track(track):
    # piano has 88 notes, corresponding to note id 21 to 108, any note out of the id range will be ignored
    result = []
    last_state, last_time = get_new_state(str(track[0]), [0]*88) # last state & time starts out as 0
    for i in range(1, len(track)): # for each message in track
        new_state, new_time = get_new_state(track[i], last_state) # get new state for the given message
        if new_time > 0: # only add if all changes for current state detected (multiple messages w/ time of 0 = multiple notes changing)
            # CALCULATE DIFFERENT NUMBER OF FRAMES TO PLAY last_state HERE
            num_ticks = int(new_time / DOWNSAMPLE_RATE)
            result += [last_state]*num_ticks # play last_state for number of ticks specified by next message; DOWNSAMPLE_RATE to decrease overall number of entries
            if ADD_BREAKS:
                result += [[0]*88] # add empty state after each message (reset for when same notes are played in a row); ERROR: THIS CREATES OFFSET IF MULTIPLE TRACKS
        last_state, last_time = new_state, new_time
    return result

# convert midi file; most of the code here is just cleanup
# mid = midi file
# min_msg_pct = if track length is below this percentage, ignore it
def convert_midi(mid, min_msg_pct=0.1):
    tracks_len = [len(tr) for tr in mid.tracks] # list of track lengths
    min_n_msg = max(tracks_len) * min_msg_pct # longest track length * min percentage = minimum track length to not get removed
    
    # convert each track to nested list
    all_arys = []
    for i in range(len(mid.tracks)): # for each track in midi file
        if len(mid.tracks[i]) > min_n_msg: # if length of track is larger than min track length, then add it
            ary_i = convert_track(mid.tracks[i]) 
            all_arys.append(ary_i)
    
    # make all nested list the same length (fill with 0s then trim afterwards)
    max_len = max([len(ary) for ary in all_arys]) # longest track
    for i in range(len(all_arys)): # for each track
        if len(all_arys[i]) < max_len: # if track length is < longest track
            all_arys[i] += [[0] * 88] * (max_len - len(all_arys[i])) # pad with 0s at the end
    all_arys = np.array(all_arys) # convert to numpy array
    all_arys = all_arys.max(axis=0) # combine into single array, take highest velocity
    # good video for visualizing what's happening: https://www.youtube.com/watch?v=XC_j0cr_a8U
    
    # trim: remove consecutive 0s in the beginning and at the end
    sums = all_arys.sum(axis=1)
    ends = np.where(sums > 0)[0] # look only at non-zero states (at least one note w/ velocity > 0)
    return all_arys[:max(ends)]
###################################

if __name__ == "__main__":
    main()
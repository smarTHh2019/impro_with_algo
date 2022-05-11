#!/usr/bin/env python
"""sonic_pi_communication.py: communicate with Sonic Pi"""

__author__      = "Thomas Heller"
__copyright__   = "Copyright 2022, Thomas Heller"

import logging
from collections import namedtuple
from typing import Tuple
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
from composing import compose_n_bars

logging.basicConfig(level=logging.INFO)

# Define a datatype for a phrase
phrase = namedtuple('phrase' , 'melo rhym')

def translate_sonic_pi_ring(ring_str:str) -> Tuple:

    # example = "[(ring <SonicPi::Chord :C :7 [60, 64, 67, 70]), (ring <SonicPi::Chord :C :7 [60, 64, 67, 70]), (ring <SonicPi::Chord :C :7 [60, 64, 67, 70]), (ring <SonicPi::Chord :C :7 [60, 64, 67, 70])]"

    tmp_1 = ring_str.replace('ring <','').replace('(','').replace(')','')
    tmp_2 = tmp_1.split('SonicPi::Chord ')[1:]
    all_chord_names, all_chord_tones = '', []
    for ch_str in tmp_2:
        name_part, number_part = ch_str.split('[')
        all_chord_names += ',' + name_part.replace(':','').replace(' ','')
        chord_tones = number_part.replace(']','').replace(' ','')
        chord_tones = chord_tones.split(',')
        all_chord_tones.append([int(ii)%12 for ii in chord_tones if ii != ''])
    
    return all_chord_names[1:], all_chord_tones

def send_phrase_to_sonic_pi(tag:str, in_phrase:phrase) -> None:
    '''Sending a phrase to Sonic Pi'''

    client = udp_client.SimpleUDPClient('127.0.0.1', 4560)
    client.send_message(f'/{tag}_melo', in_phrase.melo)
    client.send_message(f'/{tag}_rhym', in_phrase.rhym)
    logging.info(f'Sonic-Pi communicaiton: message {tag} send')

def dummy_compose_function(unused_addr, args, num_bars):
    '''This dummy function composes something'''


    logging.info(f"Tag {unused_addr} wants to dummy compose {num_bars} bars")
    send_phrase_to_sonic_pi('dummy_compose_function_2', phrase([60,64,67,65]*num_bars,[1,2,0.5,0.5]*num_bars))

def compose_test_function_1(unused_addr, args, input_chords):
    '''This dummy function composes something based on the input chords (list of ints)'''

    chord_names, chord_tones = translate_sonic_pi_ring(input_chords)

    logging.info(f"Tag {unused_addr} wants to compose {len(chord_tones)} bars as test 1")
    melo, rhym = compose_n_bars(chord_tones)
    print(f'Melody: {melo}')
    print(f'Rhythm: {rhym}')
    send_phrase_to_sonic_pi('compose_test_function_1', phrase(melo, [nn/4 for nn in rhym]))

def listen_to_phrase_request_from_sonic_pi(tag:str="/impro/phrase", compose_func=dummy_compose_function, port:int=4545) -> str:
    '''Listen on the OSC server and composes a phrase if requested
    
    tag = Name of the OSC message <> this needs to match what the Sonic Pi script sends.
          Multiple composing listeners are possible and are separated by this tag.
    compose_func = The function that will compose the improvisation.
    port = used port <> this needs to match what Sonic Pi sends on via `use_osc "localhost", 4545`
    '''

    dispatcher_var = dispatcher.Dispatcher()
    dispatcher_var.map(tag, compose_func, "TEST")
    server = osc_server.ThreadingOSCUDPServer(('127.0.0.1', 4545), dispatcher_var)
    logging.info(f'Server is running on {server.server_address[0]}, {server.server_address[1]}')
    server.serve_forever()

if __name__ == '__main__':
    # test listening to a port and composing with a specific function
    listen_to_phrase_request_from_sonic_pi(tag="/impro/phrase", compose_func=compose_test_function_1, port=4545)

    # test sending one phrase
    #send_phrase_to_sonic_pi('dummy_compose_function_2', phrase([60,61,62,63],[4,8,2,2]))

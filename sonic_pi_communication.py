#!/usr/bin/env python
"""sonic_pi_communication.py: communicate with Sonic Pi"""

__author__      = "Thomas Heller"
__copyright__   = "Copyright 2022, Thomas Heller"

import logging
from collections import namedtuple
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
from composing import compose_n_bars

logging.basicConfig(level=logging.INFO)

# Define a datatype for a phrase
phrase = namedtuple('phrase' , 'melo rhym')

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

def compose_test_function_1(unused_addr, args, num_bars):
    '''This dummy function composes something'''

    logging.info(f"Tag {unused_addr} wants to compose {num_bars} bars as test 1")
    melo, rhym = compose_n_bars(num_bars)
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

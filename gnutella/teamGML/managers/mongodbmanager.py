__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

import mongoengine

def connect():
    mongoengine.connect('Napster')
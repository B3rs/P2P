__author__ = 'LucaFerrari MarcoBersani GiovanniLodi'

DEBUG = True
UI_LOGGER = None

def klog(message):
    if DEBUG:
        print message

        if UI_LOGGER:
            UI_LOGGER.show_log_message(message)
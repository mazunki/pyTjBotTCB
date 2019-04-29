import board
import neopixel
from queue import *

WIDTH = 8
HEIGHT = 5
NUM_PIXELS = WIDTH*HEIGHT

ORDER = neopixel.GRB
PIXEL_PIN = board.D21

led_board = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=0.2, auto_write=False, pixel_order=ORDER)

led_stack = Queue(maxsize=3)
supported = dict()

def add_to_led(item):
    global led_stack
    if item in supported.keys():
        led_stack.put(item)
    else:
        print(supported)


def init_led():
    global led_board
    #led_board = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=0.2, auto_write=False, pixel_order=ORDER)
    import neopixels.matrix as matrix

    global supported
    supported = {
        "police": matrix.police,
        "rainbow": matrix.rainbow
    }

    while True:
        global led_stack
        print(list(led_stack.queue))
        if led_stack.empty() == False:
            worm_alive = False
            desired_function = led_stack.get()
            supported[desired_function]()
            print("Shining", desired_function)
        else:
            worm_alive = True
            matrix.worm()


if __name__ == "__main__":
    import sys
    sys.path.insert(0,'../')
    init_led()

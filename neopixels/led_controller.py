import board
import neopixel
from queue import *

WIDTH = 8
HEIGHT = 5
NUM_PIXELS = WIDTH*HEIGHT

ORDER = neopixel.GRB
PIXEL_PIN = board.D18

led_board = 0


led_stack = Queue(maxsize=3)
supported = dict()

def add_to_led(item):
	if item in supported.keys():
		led_stack.put(item)

def init_led():
	global led_board
	add_support()
	led_board = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=0.2, auto_write=False, pixel_order=ORDER)

	while True:
		if led_stack.empty() == False:
			matrix.worm_alive = False
			desired_function = led_stack.get()
			supported[desired_function]
		else:
			worm_alive = True
			matrix.worm()

def add_support():
	import neopixels.matrix as matrix
	global supported
	supported = {
		"police": matrix.police,
		"rainbow": matrix.rainbow
	}

add_to_led("police")
init_led()
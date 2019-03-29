import time
import board
import neopixel

NUM_PIXELS = 40
ORDER = neopixel.GRB
pixel_pin = board.D18

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
NEON = (0,255,255)
PURPLE = (255,0,255)

board = neopixel.NeoPixel(pixel_pin, NUM_PIXELS, brightness=0.2, auto_write=False, pixel_order=ORDER)



def light_led(pixels, color):
    for pixel in pixels:
        board[pixel] = color
    board.show()

def light_all(color=WHITE):
    for i in range(0,NUM_PIXELS):
        board[i] = color
    board.show()


# POLICE STUFF START
def police_half():
    light_led([i for i in range(0,NUM_PIXELS) if i%8 < 4], RED)
    light_led([i for i in range(0,NUM_PIXELS) if i%8 >= 4], BLUE)
    time.sleep(0.5)
    light_led([i for i in range(0,NUM_PIXELS) if i%8 < 4], BLUE)
    light_led([i for i in range(0,NUM_PIXELS) if i%8 >= 4], RED)
    time.sleep(0.5)

def police_fill():
    light_all(RED)
    time.sleep(0.5)
    light_all(BLACK)
    time.sleep(0.1)
    light_all(BLUE)
    time.sleep(0.5)
    light_all(BLACK)
    time.sleep(0.1)

def police():
    for _ in range(3):
        for _ in range(3):
            police_fill()
        for _ in range(3):
            police_half()
# POLICE STUFF END


police()

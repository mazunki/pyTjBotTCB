import time
import board
import neopixel

WIDTH = 8
HEIGHT = 5
NUM_PIXELS = 40

ORDER = neopixel.GRB
PIXEL_PIN = board.D18

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
NEON = (0,255,255)
PURPLE = (255,0,255)

led_board = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=0.2, auto_write=False, pixel_order=ORDER)


def light_led(pixels, color):
    for pixel in pixels:
        led_board[pixel] = color
    led_board.show()

def light_all(color=WHITE):
    for i in range(0,NUM_PIXELS):
        led_board[i] = color
    led_board.show()


# POLICE STUFF START
def police_half():
    light_led([i for i in range(0,NUM_PIXELS) if i%WIDTH < WIDTH/2], RED)
    light_led([i for i in range(0,NUM_PIXELS) if i%WIDTH >= WIDTH/2], BLUE)
    time.sleep(0.5)
    light_led([i for i in range(0,NUM_PIXELS) if i%WIDTH < WIDTH/2], BLUE)
    light_led([i for i in range(0,NUM_PIXELS) if i%WIDTH >= WIDTH/2], RED)
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

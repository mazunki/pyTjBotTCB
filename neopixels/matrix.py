import time
import board
import neopixel

WIDTH = 8
HEIGHT = 5
NUM_PIXELS = WIDTH*HEIGHT

POSITIVE_X = 1
POSITIVE_Y = 1

NEGATIVE_X = -POSITIVE_X
NEGATIVE_Y = -POSITIVE_Y

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

# Change leds
def light_led(pixels, color, coords=False):
    if isinstance(light_led, int):  # support single leds
        pixels = [pixels]

    for pixel in pixels:
        if coords:
            pixel = pixel[0]+WIDTH*pixel[1]

        led_board[pixel] = color

    led_board.show()

def light_all(color=WHITE):
    for i in range(0,NUM_PIXELS):
        led_board[i] = color
    led_board.show()

def shut_all():
    light_all(BLACK)


# Worm
def worm():
    for row in range(0,HEIGHT):
        row_pixels = [i if row%2 == 0 else WIDTH-i-1 for i in range(0,WIDTH)]  # direction per row
        for pixel in row_pixels:
            light_led([pixel, row], RED, coords=True)
            time.sleep(0.5)



# GFX POLICE START
def police():
    def police_fill():
        light_all(RED)
        time.sleep(0.5)
        light_all(BLACK)
        time.sleep(0.1)
        light_all(BLUE)
        time.sleep(0.5)
        light_all(BLACK)
        time.sleep(0.1)
    def police_half(speed=0.1):
        light_led([i for i in range(0,NUM_PIXELS) if i%WIDTH < WIDTH/2], RED)
        light_led([i for i in range(0,NUM_PIXELS) if i%WIDTH >= WIDTH/2], BLUE)
        time.sleep(speed)
        light_all(BLACK)
        light_led([i for i in range(0,NUM_PIXELS) if i%WIDTH < WIDTH/2], BLUE)
        light_led([i for i in range(0,NUM_PIXELS) if i%WIDTH >= WIDTH/2], RED)
        time.sleep(speed)
        light_all(BLACK)


    for _ in range(2):
        for _ in range(2):
            police_fill()
        for _ in range(6):
            police_half()
        light_all(BLACK)
        time.sleep(0.2)
#/ GFX POLICE end.


police()

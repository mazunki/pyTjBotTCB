import time
import board
import neopixel
import random

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

COLORS13 = [0x808080, 0xFF0000, 0x800000, 0xFFFF00, 0x808000, 0x00FF00, 0x008000, 0x00FFFF, 0x008080, 0x0000FF, 0x000080, 0xFF00FF, 0x800080]

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
            light_led([[pixel, row]], RED, coords=True)
            time.sleep(0.2)
            shut_all()


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


# GFX RAINBOW start
def wheel(pos):
    """ Rainbow wheel from Adafruit example """
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)
 
 
def rainbow_cycle(wait):
    for j in range(255):
        for i in range(NUM_PIXELS):
            pixel_index = (i * 256 // NUM_PIXELS) + j
            led_board[i] = wheel(pixel_index & 255)
        led_board.show()
        time.sleep(wait)
def rainbow():
    for _ in range(2):
        rainbow_cycle(0.001)
    light_all(BLACK)
#/ GFX RAINBOW end

# GFX SMILY start
def gfx_storm():
    light_all(BLACK)
    time_end = time.time() + 5
    while time.time() < time_end:
        for i in range(40):
            r = random.randrange(256)
            g = random.randrange(256)
            b = random.randrange(256)
            led_board[i] = (r, g, b)
            led_board.show()
        led_board.show()
        time.sleep(.1)
#/ GFS STORM end

def gfx_storm_set():
    light_all(BLACK)
    time_end = time.time() + 3
    while time.time() < time_end:
        for i in range(40):
            led_board[i] = (random.choice(COLORS13))
        led_board.show()
        time.sleep(.2)
    light_all(BLACK)

###

def cols_rows():
    row_pixels={1:(0,7),2:(8,15),3:(16,23),4:(24,31),5:(32,40)}
    for _ in range(10):
        line_color = random.choice(COLORS13)
        for i in range(8):
            for j in range(i, NUM_PIXELS, 8):
                led_board[j] = (line_color)
                led_board.show()
                light_all(BLACK)
                for l in range(j, j+8):
                    led_board[l] = (line_color)
                    led_board.show()
                    time.sleep(.2)

# Run functions

#worm()
#light_all(BLACK)
#rainbow()
#light_all(BLACK)
#police()
#light_all(BLACK)
#gfx_storm_set()
light_all(BLACK)
cols_rows()



#for _ in range(3):
#    gfx_storm()
#    light_all(BLACK)
#    gfx_storm_set()
#    light_all(BLACK)

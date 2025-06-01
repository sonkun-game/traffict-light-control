import RPi.GPIO as GPIO
import time

# South 
LED_GREEN=5
LED_YELLOW=6
LED_RED=13

# East
E_LED_GREEN=10
E_LED_YELLOW=9
E_LED_RED=11

# North
N_LED_GREEN=17
N_LED_YELLOW=27
N_LED_RED=22

# West
W_LED_GREEN=2
W_LED_YELLOW=3
W_LED_RED=4


def setup():
	# SOUTH
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(LED_GREEN, GPIO.OUT)
	GPIO.setup(LED_YELLOW, GPIO.OUT)
	GPIO.setup(LED_RED, GPIO.OUT)
	# turn off light
	GPIO.output(LED_GREEN, 0)
	GPIO.output(LED_YELLOW, 0)
	GPIO.output(LED_RED, 0)
	# EAST
	GPIO.setup(E_LED_GREEN, GPIO.OUT)
	GPIO.setup(E_LED_YELLOW, GPIO.OUT)
	GPIO.setup(E_LED_RED, GPIO.OUT)
	GPIO.output(E_LED_GREEN, 0)
	GPIO.output(E_LED_YELLOW, 0)
	GPIO.output(E_LED_RED, 0)
	# NORTH
	GPIO.setup(N_LED_GREEN, GPIO.OUT)
	GPIO.setup(N_LED_YELLOW, GPIO.OUT)
	GPIO.setup(N_LED_RED, GPIO.OUT)
	GPIO.output(N_LED_GREEN, 0)
	GPIO.output(N_LED_YELLOW, 0)
	GPIO.output(N_LED_RED, 0)
	# WEST
	GPIO.setup(W_LED_GREEN, GPIO.OUT)
	GPIO.setup(W_LED_YELLOW, GPIO.OUT)
	GPIO.setup(W_LED_RED, GPIO.OUT)
	GPIO.output(W_LED_GREEN, 0)
	GPIO.output(W_LED_YELLOW, 0)
	GPIO.output(W_LED_RED, 0)
	

# EAST
def turn_east_light(color):
	GPIO.output(E_LED_GREEN, 0)
	GPIO.output(E_LED_YELLOW, 0)
	GPIO.output(E_LED_RED, 0)
	if color == 'green' :
		
		GPIO.output(E_LED_GREEN, 1)
		print('green')
	elif color == 'yellow' :
		GPIO.output(E_LED_YELLOW, 1)
		print('yellow')
	elif color == 'red' :
		GPIO.output(E_LED_RED, 1)
		print('red')
		
# WEST
def turn_west_light(color):
	GPIO.output(W_LED_GREEN, 0)
	GPIO.output(W_LED_YELLOW, 0)
	GPIO.output(W_LED_RED, 0)
	if color == 'green' :
		
		GPIO.output(W_LED_GREEN, 1)
		print('green')
	elif color == 'yellow' :
		GPIO.output(W_LED_YELLOW, 1)
		print('yellow')
	elif color == 'red' :
		GPIO.output(W_LED_RED, 1)
		print('red')
		
# NORTH
def turn_north_light(color):
	GPIO.output(N_LED_GREEN, 0)
	GPIO.output(N_LED_YELLOW, 0)
	GPIO.output(N_LED_RED, 0)
	if color == 'green' :
		
		GPIO.output(N_LED_GREEN, 1)
		print('green')
	elif color == 'yellow' :
		GPIO.output(N_LED_YELLOW, 1)
		print('yellow')
	elif color == 'red' :
		GPIO.output(N_LED_RED, 1)
		print('red')
		
# SOUTH
def turn_south_light(color):
	GPIO.output(LED_GREEN, 0)
	GPIO.output(LED_YELLOW, 0)
	GPIO.output(LED_RED, 0)
	if color == 'green' :
		
		GPIO.output(LED_GREEN, 1)
		print('green')
	elif color == 'yellow' :
		GPIO.output(LED_YELLOW, 1)
		print('yellow')
	elif color == 'red' :
		GPIO.output(LED_RED, 1)
		print('red')
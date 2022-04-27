# imports
from machine import Pin, I2C, ADC, PWM
from ssd1306 import SSD1306_I2C
import math
from time import sleep

w = 128 # width of screen
h = 32 # height of screen
buzzer=PWM(Pin(13))

# pin assignments
i2c = I2C(0, scl=Pin(1), sda = Pin(0), freq = 200000)
addr = i2c.scan()[0]
oled = SSD1306_I2C(w,h,i2c, addr)
adc = ADC(Pin(26))
button = Pin(20, Pin.IN, Pin.PULL_DOWN)
r_led = Pin(16, Pin.OUT)
u_led = Pin(14, Pin.OUT)
g_led = Pin(15, Pin.OUT)

# define vars
x=0
y=0
x2=0
y2=0
wave_type="sin"
buzzer_on = False

# reset led
r_led.value(0)
g_led.value(0)
u_led.value(1)


#method definitions
def normalize(a, b): # changes the hertz value so it is compatible with oled screen size
    return float(b/a)

def toggle_wave(wave): # changes the wave from sin to cos
    print(wave)
    if wave== "sin": # when wave is cos, g_led is on
        wave="cos"
        u_led.value(0)
        g_led.value(1)
    elif wave == "cos": # when wave is sin, u_led is on
        wave="sin"
        g_led.value(0)
        u_led.value(1)
    return wave #returns the correct value

def start_up_noise():
    ''' plays a windows startup noise '''
    buzzer.duty_u16(1000)
    buzzer.freq(622) #Eb
    sleep(0.375)
    buzzer.freq(311) #Eb
    sleep(0.25)
    buzzer.freq(932) #Bb
    sleep(0.25)
    buzzer.freq(831) #Ab
    sleep(0.25)
    buzzer.freq(622) #Eb
    sleep(0.25)
    buzzer.freq(466) #Bb
    sleep(0.375)
    buzzer.duty_u16(0)
    

start_up_noise()
while True:
    x2=0
    y2=0
    for x in range(0, w):
        if button.value(): #checks if the button is pressed
#             wave_type=toggle_wave(wave_type) # switches the type of wave
            if buzzer_on:
                buzzer_on=False
                buzzer.duty_u16(0)
                u_led.value(0)
                g_led.value(1)
            else:
                buzzer_on=True
                buzzer.duty_u16(500)
                g_led.value(0)
                u_led.value(1)
            sleep(0.5)
    
        hertz = round((adc.read_u16()/2340.53571429)) # turns the potentiometer output into 2-28 hertz
        if hertz<2: hertz=2 # sets the minumum hertz value
        hertz_as_degrees = math.degrees(math.pi * hertz) # turns the hertz into degrees of circle
        normalized_x = x * normalize(w, hertz_as_degrees) # adjusts for small oled screen
        rads_x = math.radians(normalized_x) # turns degrees into radians
        if wave_type=="sin":
            y = int(math.sin(rads_x) * (h/2)) # sets y value to sin output
        elif wave_type=="cos":
            y = int(math.cos(rads_x) * (h/2)) # sets y value to cos output
        oled.pixel(x,y+16,1) # draws waave
        oled.line(x,y+16,x2,y2+16,1)
        x2=x
        y2=y
        oled.show()
        adjusted_hertz = int(hertz*31.4)
#         print(f"{hertz}, {adjusted_hertz}")
#         print(adc.read_u16())
#         print(f"{x}, {y}")
        buzzer.freq(adjusted_hertz)
        sleep(0.005)
    oled.fill(0)
    
    
    
    # TODO: 
    #       make pretty
    #       power


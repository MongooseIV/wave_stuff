# imports
from machine import Pin, I2C, ADC, PWM
from ssd1306 import SSD1306_I2C
import math
from time import sleep

w = 128 # width of screen
h = 32 # height of screen

def getFrequency(note, A4=440): #credit for function to Charles Grassin
    notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

    octave = int(note[2]) if len(note) == 3 else int(note[1])
        
    keyNumber = notes.index(note[0:-1]);
    
    if (keyNumber < 3) :
        keyNumber = keyNumber + 12 + ((octave - 1) * 12) + 1; 
    else:
        keyNumber = keyNumber + ((octave - 1) * 12) + 1; 

    return A4 * 2** ((keyNumber- 49) / 12)

# pin assignments
buzzer=PWM(Pin(7))
b2=PWM(Pin(25))
b3=PWM(Pin(26))
b4=PWM(Pin(27))
i2c = I2C(0, scl=Pin(1), sda = Pin(0), freq = 200000)
addr = i2c.scan()[0]
oled = SSD1306_I2C(w,h,i2c, addr)
adc = ADC(Pin(26))
pr_adc = ADC(Pin(27))
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
    b2.duty_u16(1000)
    b3.duty_u16(1000)
    b4.duty_u16(1000)
    buzzer.freq(round(getFrequency("D#5"))) #Eb
    b2.freq(round(getFrequency("A#3")))
    b3.freq(round(getFrequency("C3")))
    b4.freq(round(getFrequency("D#2"))) 
    sleep(0.375)
    buzzer.freq(round(getFrequency("D#4"))) #Eb
    sleep(0.25)
    buzzer.freq(round(getFrequency("A#4"))) #Bb
    b2.freq(round(getFrequency("A#3")))
    b3.freq(round(getFrequency("D#3")))
    b4.freq(round(getFrequency("G#2"))) 
    sleep(0.25)
    buzzer.freq(round(getFrequency("G#4"))) #Ab
    sleep(0.25)
    buzzer.freq(round(getFrequency("D#5"))) #Eb
    b2.freq(round(getFrequency("D#3")))
    b3.freq(round(getFrequency("A#2")))
    b4.freq(round(getFrequency("D#2"))) 
    sleep(0.25)
    buzzer.freq(round(getFrequency("A#4"))) #Bb
    sleep(0.375)
    buzzer.duty_u16(0)
    sleep(0.5)
    b2.duty_u16(0)
    b3.duty_u16(0)
    b4.duty_u16(0)
    

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
                buzzer.duty_u16(1000)
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


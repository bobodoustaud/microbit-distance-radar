#loading libraries
#use "vittascience" website to bake the code due to the use of the 'lcd_12c' micropython library used. I could not find the source code of it. See "https://fr.vittascience.com/microbit/?mode=code&console=bottom&toolbox=vittascience"
from microbit import *
from lcd_i2c import LCD1602
import machine
import microbit
import music
#loading global variables
lcd = LCD1602()
x=0
menu=True
spd=True
a=[]
#characters used for quarter values of progression
b=['|','&','@','#']
lcd.setCursor(0,0)
#plays async sound
def sound():
  music.play(['a:2'], pin=pin0, wait=False)
#calculates distance by multiplying time elapsed between pings and speed of sound. Sensor MUST be in 3rd slot of the i/o shield
def dist():
  microbit.pin1.write_digital(1)
  sleep(0.1)
  microbit.pin1.write_digital(0)
  #waiting for ping
  while not microbit.pin1.read_digital() == 1:
    return machine.time_pulse_us(pin1, 1)*0.00034029
distance=dist()
#loading progress bar array
for i in range(64):
  if i%4==0:
    y=""
    for _ in range(int(i/4)):
      y=y+"#"
    for _ in range(4):
      a.append(y)
  a[i]=str(a[i])+b[i%4]
#setting first value of array as empty

a.insert(0,'')
#main loop
while True:
  #menu button
  if button_a.was_pressed():
    sound()
    lcd.clear()
    menu=not menu
  #menu code
  if menu==True:
    lcd.setCursor(0,0)
    lcd.writeTxt("Select mode:")
    #changing mode if b is pressed "normal" mode is the requested values and "maximum" mode is the maximum amount that the sensor is able to realistically measure
    if button_b.was_pressed() :
      sound()
      spd=not spd
      lcd.clear()
    lcd.setCursor(0,1)
    if spd==True:
      lcd.writeTxt("Normal")
    else:
      lcd.writeTxt("Maximum")
  #sensor render
  else:
    #x is looping
    x=x+1
    sleep(10)
    #distance is used instead of dist() to only call the function once per loop and prevent unintended behavior from the physical sensor and to enhance reliability and response time
    distance=dist()
    #failure-proofing the code due to the occasional miss of the ping
    try:
      lcd.setCursor(0,0)
      #loading right value from array and displaying it
      #in conditional operator, first value is used as max distance for the progress bar for spd==True (or "normal" mode) and second value is used for "maximum" value
      lcd.writeTxt(a[int(distance*100/((150. if spd==True else 300.)/64))]+"                 ")
    #handling array index out of range issue with too high values
    except:
      lcd.writeTxt("################")
    #only actualising number render every 20 loops to make the number readable on low-quality displays and to prevent unreadable erratic numbers
    if x>=20:
      lcd.setCursor(0,1)
      #fail-proofing again if distance is undefined due to physical failure of the sensor
      #blank 16 spaces used to cleanse screen of old characters
      try:
        lcd.writeTxt(str(distance*100)+" cm"+"                ")
      except:
        lcd.writeTxt("                ")
      x=0
    #making noise if distance less than certain amount, 30 cm in this case
    try:
      if distance<0.3:
        sound()
    #printing in console "missing bounce" if the sensor fails
    except:
      print("missing bounce")

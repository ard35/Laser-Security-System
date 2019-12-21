import RPi.GPIO as GPIO
import Keypad
import smbus
import time
import math

ROWS = 4        # number  of rows of the  Keypad
COLS = 4        #number  of columns  of the Keypad
keys =  [   '1','2','3','A',    #key code
'4','5','6','B',
'7','8','9','C',
'*','0','#','D'     ]

rowsPins = [12,16,18,22]    #connect  to the  row pinouts  of the  keypad
colsPins = [37,15,13,11]      #connect  to the  column  pinouts of the  keypad

buzzerPin = 29 # defines the buzzerPin
redledPin = 38
greenledPin = 40
yellowledPin = 36

address = 0x48
bus=smbus.SMBus(1)
cmd=0x40

def analogRead(chn):
 value = bus.read_byte_data(address,cmd+chn)
 return value

def analogWrite(value):
 bus.write_byte_data(address,cmd,value) 

def setup():    
  print ('Program is starting...')  # printing starting message     
  GPIO.setmode(GPIO.BOARD)          # Number GPIOs by physical location     
  GPIO.setup(buzzerPin, GPIO.OUT)   # Set buzzerPin as output
  GPIO.setup(redledPin, GPIO.OUT)         # Set redledPin mode to output
  GPIO.output(redledPin, GPIO.LOW)      # Set redledPin low to off led (initial condition)
  GPIO.setup(greenledPin, GPIO.OUT)         # Set greenledPin mode to output
  GPIO.output(greenledPin, GPIO.LOW)      # Set greenledPin low to off led (initial condition)
  GPIO.setup(yellowledPin, GPIO.OUT)         # Set yellowledPin mode to output
  GPIO.output(yellowledPin, GPIO.LOW)      # Set yellowledPin low to off led (initial condition)

def loop():
    password = '2222'
    entered = ''
    check = -1
    trip = 1
    keypad  = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS)    #createKeypad object
    keypad.setDebounceTime(50)       #set the debounce  time
    
    while check == -1:
        value = analogRead(0)        #read A0 pin
        print (value)
        time.sleep(0.1)
        if value <= 99:
            value = analogRead(0)        #read A0 pin
            time.sleep(0.1)
            print ('System OK')
            GPIO.output(buzzerPin,GPIO.LOW)     # silence buzzer 
            GPIO.output(buzzerPin,GPIO.LOW)
            GPIO.output(greenledPin, GPIO.HIGH)  # greenled on
            GPIO.output(redledPin, GPIO.LOW)   # led off
            GPIO.output(yellowledPin, GPIO.LOW)   # led off
            

        if value > 99:
            value = analogRead(0)        #read A0 pin
            time.sleep(0.1)
            trip = -1
            while (trip == -1):
                value = analogRead(0)        #read A0 pin
                time.sleep(0.1)
                print ('INTRUDER!')
                GPIO.output(buzzerPin,GPIO.HIGH)     # sounds the buzzer 
                GPIO.output(buzzerPin,GPIO.HIGH) # sounds the buzzer
                GPIO.output(redledPin, GPIO.HIGH)  # redled on
                GPIO.output(greenledPin, GPIO.LOW)   # led off
                GPIO.output(yellowledPin, GPIO.LOW)   # led off
                key = keypad.getKey()       #obtain  the state of keys
                if(key != keypad.NULL):  
                    entered = entered + key
                    if len(entered) == 4:
                        if entered == password:
                            check = check * -1
                            trip = trip * -1
                        else:
                            entered == ''
                            check = check
            
        
        if check == 1:
            print ('System OFF')
            GPIO.output(yellowledPin, GPIO.HIGH)  # yellowled on
            GPIO.output(redledPin, GPIO.LOW)   # led off
            GPIO.output(greenledPin, GPIO.LOW)   # led off
            GPIO.output(buzzerPin,GPIO.LOW)     # silence buzzer 
            if(key != keypad.NULL):  
                    entered = entered + key
                    if len(entered) == 4:
                        if entered == password:
                            check = check * -1
                            trip = trip * -1
                        else:
                            entered == ''
                            check = check
            
            

def destroy():
    GPIO.output(buzzerPin, GPIO.LOW) # turns buzzer off
    GPIO.output(redledPin, GPIO.LOW)     # led off
    GPIO.output(yellowledPin, GPIO.LOW)     # led off
    GPIO.output(greenledPin, GPIO.LOW)     # led off 
    GPIO.cleanup() # Release resources
    bus.close() 
 
if __name__ == '__main__': # Program start from here
  setup()
  try:
    loop()
  except KeyboardInterrupt: # When 'Ctrl+C' is pressed, the child program destroy() will be executed.
    destroy() 
# Laser-Security-System
This is a PYTHON program, which is uploaded to a Raspberry Pi using the Thonny IDE. 

A photoresistor checks for a laser light. 

In normal conditions, a green LED and a shell message of "System OK" is produced. 
If the laser is crossed, a red LED, a buzzer sound, and a shell message of "INTRUDER" is produced, and stays in this state until the password is entered into a keypad. Upon entry of the password, it will check if it is correct. 
If correct, the system will turn OFF, a yellow LED and a shell message of "System OFF" will be produced. Re-run the program to initiate the system to ON once more. 

A picture of the schematics are included, along with the original Fritzing file.
This program does need the inclusion of the Keypad library. I did not write this library, but I have attached it.

**School Project**

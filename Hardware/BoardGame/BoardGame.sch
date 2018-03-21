EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:switches
LIBS:relays
LIBS:motors
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:ws2811
LIBS:BoardGame-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Conn_02x20_Counter_Clockwise J?
U 1 1 5AAB910B
P 2050 5500
F 0 "J?" H 2100 6500 50  0000 C CNN
F 1 "Conn_02x20_Counter_Clockwise" H 2100 4400 50  0000 C CNN
F 2 "" H 2050 5500 50  0001 C CNN
F 3 "" H 2050 5500 50  0001 C CNN
	1    2050 5500
	-1   0    0    1   
$EndComp
$Comp
L ws2811 U?
U 1 1 5AABB194
P 5850 2250
F 0 "U?" H 5800 2400 60  0000 C CNN
F 1 "ws2811" H 5800 2400 60  0000 C CNN
F 2 "" H 5800 2400 60  0001 C CNN
F 3 "" H 5800 2400 60  0001 C CNN
	1    5850 2250
	1    0    0    -1  
$EndComp
Wire Wire Line
	2250 4500 2800 4500
Text Label 2250 4500 0    60   ~ 0
PWR_3.5mm
$Comp
L Audio-Jack-3 J?
U 1 1 5AABCE60
P 8000 1450
F 0 "J?" H 7950 1625 50  0000 C CNN
F 1 "Audio-Jack-3" H 8100 1380 50  0000 C CNN
F 2 "" H 8250 1550 50  0001 C CNN
F 3 "" H 8250 1550 50  0001 C CNN
	1    8000 1450
	0    1    1    0   
$EndComp
$EndSCHEMATC
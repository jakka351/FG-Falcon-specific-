#!/usr/bin/python3
#// Ford FG can0hvac
#https://github.com/jakka351/FG-Falcon/
#pip3 install regex uinput evdev os queue python-can time
import can 
import time
import os
import uinput 
import queue
import sys, traceback
from threading import Thread
#############################
c                      = ''
count                  = 0  
#############################
HVAC                    =  0x353 #can id 851 
HVAC_off                =  0xAB  #  [5] A 129 0 0 34 [171] 0 0    All Off
HVAC_TEMP               =  0     #851 x4
HVAC_OUT                =  0     #Outside Temp 851 x5
HVAC_FANSPEED           =  0     #Fan speed 851 x8
HVAC_VENTSTATUS         =  0     #Vent tatus 851 x1
VA                      =  0x4B  # print('Foot Vents, Close Cabin')
VB                      =  0x2B  # print('Foot Vents, Open Cabin')
VC                      =  0x2F  # print('Window and Feet Vets, Open Cabin')
VD                      =  0x4F  # print('Window and Feet Vents, Close Cabin')
VE                      =  0x5B  # print('Face, Foot, Close Cabin')
VF                      =  0x3B  # print('Face, Foot, Open Cabin')
VG                      =  0x33  # print('Face, Open Cabin')
VH                      =  0x53  # print('Face, Close Cabin')
VI                      =  0x27  # print('Window, Manual Fan')
VJ                      =  0x26  # print('Window, Auto Fan')
VK                      =  0x83  # print('A/C Off, Open Cabin')
VL                      =  0x8B  # print('A/C Off, Foot Vents, Open Cabin')
VM                      =  0x8F  # print('A/C Off, Foot and Window Vents, Open Cabin')
VN                      =  0x9B  # print('A/C Off, Foot and Face Vents, Open Cabin')
VO                      =  0xA6  # print('A/C Off, Window Vents, Open Cabin')
VP                      =  0xA7  # print('A/C Off, Manual Fan, Open Cabin')
VQ                      =  0xC3  # print('A/C Off, Close Cabin')
VR                      =  0xCB  # print('A/C Off, Foot Vents, Close Cabin')
VS                      =  0xCF  # print('A/C Off, Foot and Window Vents, Close Cabin')
VT                      =  0xDB  # print('A/C Off, Foot and Face Vents, Close Cabin')
VU                      =  0x43  # print('Auto, Close Cabin')
VW                      =  0x23  # print('Auto, Open Cabin')
#############################
def scroll():
    global bus
    print('  ')
    print(',,,,,,:,,,,,,,777I77II??~++++=~::,,,,::::::::::~~~==+~:::::,,::,:+?????????+==:,::::::::,:::::::::::::::::::::~~~~~~~:::')
    print(':::::::,,,,,IIIIII,IIII+~..,,:,,,,,:~:,,.....,~,,:::~+?+?=??+=~:...,,.,.,...,,,.,,,,:~?:::::::::~~~~~~::::,:::::~::::::~')
    print('::::::::::=I7777I=IIIIII~...:===,:,=~:,,,,,,::=,,,:::~~:=?===~,::::::::,,:,,:::,,,,,~=+?=,,:::::~~~~~~~==~~~~~~~:::~~~~~')
    print('::::::~=,?I?777II7IIIII=~,.,,,,,,,,,,,:,,,,,,::,,,,~:~~~~:~+:~:~~::,:~~~:::::,~,,,,,:~~=+?~~~~~==::::,~~~~~~~::::::::~~~')
    print('~~~~~~I=I?IIIIII~IIIIIII+:..,,,,,,,,,,,,.,.,,::.,,,,:::~~=~:=+~?~~::~:::~::~:...:,,:::::==:+?:+??+=?+=::::::::::::~~~~~~')
    print('======I77?+?IIIIIIIII7I7=~,.,,,..,,,,.,.,.......,.,.,.,..,,,:~=~:==~~~~~~~~~~~~~::,,:+???III?+???II??~:.~:::~~~~:::~:~:~')
    print('+++=++=I7777I?+???IIIIII+=:..,,,,,,,,,,,...,,,,,,,,,,,,..,,,:..:?I7+...,,,,,:~=~~:::::::,,,,,,,==???+~=+,?+?=::~~~~~~~~~')
    print('?????+=+=I7777I=~~+~:~IIII~,..,,,,,,,,,,..,,,,,...~+II?I?+?III7IIII777I7=............,:~:::::,,,,,,.,I?????+,?+II,::::::')
    print('??????==++++III=~~~::~+I:+?~:.........:+IIIIIIII+=?IIIIIII???????????III7II7I..........,=~::,.,:::,,,,,.,??+????++=:::::')
    print('??III?+=======::,,,,...,,:=?==~?+?????????????+==~~~~~===+++++++++++++++???II?III.....+...,,,,..,:....,:,,,,?+????I~~~~~')
    print('??III?+=======+=~=I7III~:~~I??++??IIIIII??+??++++==~~~~:::~~~~============++?II?+7II.~..,,,,:::,..,........:=77I??,==~~~')
    print('???II??+=====~~~=~~~+III~~=III??++++=+++?II??+=+?+====~~~:::::~~~~~~~~~~======+???++II.:,:,,,,~~,.,+~,......,III?:=?:,,,')
    print('+??II??+=?=~~~~~~~~~~=~I=77I7III??++==~++++=+I??+?~?+===~~~~::::::~~~~~~~~~~~===++++=II,,:,::,.:,....,..,,,~~~++,,,:::::')
    print('???III??+=++=~~~~~~~~~~~?I777IIII??++====~======????+==+==~~~~:::::::::~~~~~~~~~====+==I,:,,,:~:,...,,....,:...::::~::~~')
    print('IIIIII?I+=~~=++~~~~~~~~=?=:+IIIII??++++===~:~~~~~~~=???=?:=~~~~~::::::::~~~~~~~~~~=~=+?7~::~~=~,,...,,,.,,,,,,,,,:::::::')
    print('IIIIII??+=~~~~=++~~~~~+???~=?7II??+++++++==~~:~~~~~~:~~???=+:~~~~~~:::::::::~~~~=++:,.,+=,,,,.,.,,,,,,,,,,,,,,,:::::::::')
    print('IIII??++=?I+~~~==++~~:+??~====+I?+===+++++==~~~::::::::::~????~~~~~:::::~:~==+:,,,,?..::+=:::::::,,,,,,,,,,,::::::::::::')
    print('II????++~~=?I=~~~==++=+++~==:,~~=+====+++++:,,...:,::~:::::~~~~+~:~~:~~==,.,,.?I~,..::~~=,::::::::::::::::::::::::::::::')
    print('???????+++=~=+I?=~~=~+++~~=...,~:=+====++?:~+=?I~,I=I??..~III7I:==~,.,,.,,.,,,...::~~++~:~::::::::::::::::::::::::::::::')
    print('??????++++=~:~~?I+=~~~~+~~~.:+,,,:=+===+++~+==~=+:III=?I?77777I~~~===,,,,.,.,,~~~~=+=~::,,::::::::::::::::::::::::::::::')
    print('++===~~:::,,,,,=~?I+=:~~~~~~,,+:,,+==~+++++,:~~:==,??,:,,=??I++,,,:~===,,,::~~=++=:::~=..,,:::::::::::::::::::::::::::::')
    print('::,:::::::,,,,,,,:=+?==~~~~.=:~~,..,=+++++=~:=+=~:.,:,,,,::?=I=:::::+~====++++=~:::?I+?,..,:::::::::::::::::::::::::::::')
    print(':::::::::::::::,,,,~+====~:,,,:=,.,,,~~===~~~,:==~~~~~~:..,,,,,,..,,,~==+++~:,~++I++II?...::::::::::::::::::::::::::::::')
    print('::::::::::::::::,,,,,,+==+,:..:==.:,,~:~~~~~:,,,,:~~~~~~~~=========~++++~,....II+II+?...,:,,,,:,,:::::::::::::::::::::::')
    print(':::::::::::::::::,,,,,,,++.,,.,,,,=:,,~:::~:::,,,,,,,,,::~~~=====~====~.......?I=I.....,:~,,::::::::::::::::::::::::::::')
    print(':::::::::::::::::::::,,,,,,:~::,~+I+,..~::::::,,,,,,,,,,,,,,,,,~==~~~.........+.......,:,,,,::::::::::::::::::::::::::::')

    time.sleep(0.05)

    print('───────────────────────────────────────────────────  ───  ───  ───  ───  ───   ───  ')

    time.sleep(0.05)
    
    print(' ███████  ██████      ███████  █████  ██       ██████  ██████  ███    ██ ')
    time.sleep(0.05)
    print(' ██      ██           ██      ██   ██ ██      ██      ██    ██ ████   ██ ')
    time.sleep(0.05)
    print(' █████   ██   ███     █████   ███████ ██      ██      ██    ██ ██ ██  ██ ')
    time.sleep(0.05)
    print(' ██      ██    ██     ██      ██   ██ ██      ██      ██    ██ ██  ██ ██ ')
    time.sleep(0.05)
    print(' ██       ██████      ██      ██   ██ ███████  ██████  ██████  ██   ████ ')
    time.sleep(1.0)

    print('    ╔═╗╦ ╦╔╦╗╦ ╦╔═╗╔╗╔   ╔═╗╔═╗╔╗╔  ╦ ╦╦  ╦╔═╗╔═╗  ╔═╗╔═╗╦═╗╦╔═╗╔╦╗')
    time.sleep(0.08)
    print('    ╠═╝╚╦╝ ║ ╠═╣║ ║║║║───║  ╠═╣║║║  ╠═╣╚╗╔╝╠═╣║    ╚═╗║  ╠╦╝║╠═╝ ║ ')
    time.sleep(0.08)
    print('    ╩   ╩  ╩ ╩ ╩╚═╝╝╚╝   ╚═╝╩ ╩╝╚╝  ╩ ╩ ╚╝ ╩ ╩╚═╝  ╚═╝╚═╝╩╚═╩╩   ╩ ')

    print('         ')

    print('               https://github.com/jakka351/fg-falcon')
    
    print('          ')
    time.sleep(0.08)


    print('  ┌─┐┌─┐┌┐┌┌┬┐┬─┐┌─┐┬  ┬  ┌─┐┬─┐  ┌─┐┬─┐┌─┐┌─┐  ┌┐┌┌─┐┌┬┐┬ ┬┌─┐┬─┐┬┌─  ')
    time.sleep(0.15)
    print('  │  │ ││││ │ ├┬┘│ ││  │  ├┤ ├┬┘  ├─┤├┬┘├┤ ├─┤  │││├┤  │ ││││ │├┬┘├┴┐  ')
    time.sleep(0.15)
    print('  └─┘└─┘┘└┘ ┴ ┴└─└─┘┴─┘┴─┘└─┘┴└─  ┴ ┴┴└─└─┘┴ ┴  ┘└┘└─┘ ┴ └┴┘└─┘┴└─┴ ┴  ')
    time.sleep(0.15)
    print('                                                                                    ')
    time.sleep(0.5)
    print('───────────────────────────────────────────────────  ───  ───  ───  ───  ───   ───  ')
                                                          
    time.sleep(4.0)        

def scroll2():
    print('───────────────────────────────────────────────────  ───  ───  ───  ───  ───   ───  ')

    time.sleep(0.05)
    
    print(' ███████  ██████      ███████  █████  ██       ██████  ██████  ███    ██ ')
    time.sleep(0.05)
    print(' ██      ██           ██      ██   ██ ██      ██      ██    ██ ████   ██ ')
    time.sleep(0.05)
    print(' █████   ██   ███     █████   ███████ ██      ██      ██    ██ ██ ██  ██ ')
    time.sleep(0.05)
    print(' ██      ██    ██     ██      ██   ██ ██      ██      ██    ██ ██  ██ ██ ')
    time.sleep(0.05)
    print(' ██       ██████      ██      ██   ██ ███████  ██████  ██████  ██   ████ ')
    time.sleep(1.0)

    print('    ╔═╗╦ ╦╔╦╗╦ ╦╔═╗╔╗╔   ╔═╗╔═╗╔╗╔  ╦ ╦╦  ╦╔═╗╔═╗  ╔═╗╔═╗╦═╗╦╔═╗╔╦╗')
    time.sleep(0.08)
    print('    ╠═╝╚╦╝ ║ ╠═╣║ ║║║║───║  ╠═╣║║║  ╠═╣╚╗╔╝╠═╣║    ╚═╗║  ╠╦╝║╠═╝ ║ ')
    time.sleep(0.08)
    print('    ╩   ╩  ╩ ╩ ╩╚═╝╝╚╝   ╚═╝╩ ╩╝╚╝  ╩ ╩ ╚╝ ╩ ╩╚═╝  ╚═╝╚═╝╩╚═╩╩   ╩ ')

    print('         ')

    print('               https://github.com/jakka351/fg-falcon')
    
    print('          ')
    time.sleep(0.08)


    print('  ┌─┐┌─┐┌┐┌┌┬┐┬─┐┌─┐┬  ┬  ┌─┐┬─┐  ┌─┐┬─┐┌─┐┌─┐  ┌┐┌┌─┐┌┬┐┬ ┬┌─┐┬─┐┬┌─  ')
    time.sleep(0.15)
    print('  │  │ ││││ │ ├┬┘│ ││  │  ├┤ ├┬┘  ├─┤├┬┘├┤ ├─┤  │││├┤  │ ││││ │├┬┘├┴┐  ')
    time.sleep(0.15)
    print('  └─┘└─┘┘└┘ ┴ ┴└─└─┘┴─┘┴─┘└─┘┴└─  ┴ ┴┴└─└─┘┴ ┴  ┘└┘└─┘ ┴ └┴┘└─┘┴└─┴ ┴  ')
    time.sleep(0.15)
    print('                                                                                    ')
    time.sleep(0.5)
    print('───────────────────────────────────────────────────  ───  ───  ───  ───  ───   ───  ')
    print("    ")
    print("    ")
    print("    ")
    print("    ")
    print("    ")
    print("    ")
    print("    ")
    print("    ")

def setup():
    global bus
#   os.system("sudo /sbin/ip link set can0 type can bitrate 125000 triple-sampling on restart-ms 1000")
#   os.system("sudo /sbin/ifconfig can0 up txqueuelen 100")
    try:
        bus = can.interface.Bus(channel='vcan0', bustype='socketcan_native')
    except OSError:
        sys.exit()
    
    print("CANbus active on", bus)  

def cleanline():
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')

def cleanscreen():
    os.system("clear")

def msgbuffer():  # Recv can frames only with CAN_ID specified in SWC variable
    global message, q                                               
    while True:
        message = bus.recv()
        if message.arbitration_id == HVAC: #CAN_ID variable
            q.put(message)          # Put message into queue


def main():
    try:
        while True:
            for i in range(8):
                while(q.empty() == True):       # Wait until there is a message
                    pass
                message = q.get()
                if message.arbitration_id == HVAC:
                    cleanline()
                    cleanline()
                    cleanline()
                    cleanline()
                    print('───────────────────────────────────────────────────  ───  ───  ───  ───  ───   ───  ')
                    print('                                          ╔═╗╦╦═╗╔═╗╔═╗╔╗╔  ╔╦╗╔═╗╔╦╗╔═╗  ┌─┐')
                    print('                                          ╠═╣║╠╦╝║  ║ ║║║║   ║ ║╣ ║║║╠═╝  │  ')
                    print('                                          ╩ ╩╩╩╚═╚═╝╚═╝╝╚╝   ╩ ╚═╝╩ ╩╩    └─┘')
                    print(message.data[3] / 2)
                    time.sleep(2)
                    cleanline()
                    cleanline()
                    cleanline()
                    cleanline()
                    cleanline()
                    print('                                                      ───  ───  ───  ───  ───   ───  ')
                    print('                                          ╔╦╗╔═╗╔╦╗╔═╗  ╔═╗╦ ╦╔╦╗╔═╗╦╔╦╗╔═╗  ┌─┐')
                    print('                                           ║ ║╣ ║║║╠═╝  ║ ║║ ║ ║ ╚═╗║ ║║║╣   │  ')
                    print('                                           ╩ ╚═╝╩ ╩╩    ╚═╝╚═╝ ╩ ╚═╝╩═╩╝╚═╝  └─┘')
                    print(message.data[4])
                    time.sleep(2)
                    cleanline()
                    cleanline()
                    cleanline()
                    cleanline()
                    cleanline()
                    print('                                                      ───  ───  ───  ───  ───   ───  ')
                    print('                                          ╔═╗╔═╗╔╗╔  ╔═╗╔═╗╔═╗╔═╗╔╦╗  ')
                    print('                                          ╠╣ ╠═╣║║║  ╚═╗╠═╝║╣ ║╣  ║║  ')
                    print('                                          ╚  ╩ ╩╝╚╝  ╚═╝╩  ╚═╝╚═╝═╩╝  ')
                    print(message.data[7])
                    time.sleep(2)
                    cleanline()
                    cleanline()
                    cleanline()
                    cleanline()
                    cleanline()
                    print('                                                      ───  ───  ───  ───  ───   ───  ')
                    print('                                         ╦  ╦╔═╗╔╗╔╔╦╗  ╔═╗╔╦╗╔═╗╔╦╗╦ ╦╔═╗')
                    print('                                         ╚╗╔╝║╣ ║║║ ║   ╚═╗ ║ ╠═╣ ║ ║ ║╚═╗')
                    print('                                          ╚╝ ╚═╝╝╚╝ ╩   ╚═╝ ╩ ╩ ╩ ╩ ╚═╝╚═╝')
                    if message.data[0] == VA:
                        print('Foot Vents, Close Cabin')
                    elif message.data[0] == VB:
                        print('Foot Vents, Open Cabin')
                    elif message.data[0] == VC: 
                        print('Window and Foot Vents, Open Cabin')
                    elif message.data[0] == VD:
                        print('Window and Foot Vents, Close Cabin')
                    elif message.data[0] == VE:
                        print('Face, Foot, Close Cabin')
                    elif message.data[0] == VF:
                        print('Face, Foot, Open Cabin')
                    elif message.data[0] == VG:
                        print('Face, Open Cabin')
                    elif message.data[0] == VH: 
                        print('Face, Close Cabin')
                    elif message.data[0] == VI: 
                        print('Window, Manual Fan')
                    elif message.data[0] == VJ: 
                        print('Window, Auto Fan')
                    elif message.data[0] == VK:
                        print('A/C Off, Open Cabin')
                    elif message.data[0] == VL:
                        print('A/C Off, Foot Vents, Open Cabin')
                    elif message.data[0] == VM:
                        print('A/C Off, Foot and Window Vents, Open Cabin')
                    elif message.data[0] == VN:
                        print('A/C Off, Foot and Face Vents, Open Cabin')
                    elif message.data[0] == VO:
                        print('A/C Off, Window Vents, Open Cabin')
                    elif message.data[0] == VP:
                        print('A/C Off, Manual Fan, Open Cabin')
                    elif message.data[0] == VQ:
                        print('A/C Off, Close Cabin')
                    elif message.data[0] == VR:
                        print('A/C Off, Foot Vents, Close Cabin')
                    elif message.data[0] == VS:
                        print('A/C Off, Foot and Window Vents, Close Cabin')
                    elif message.data[0] == VT:
                        print('A/C Off, Foot and Face Vents, Close Cabin')
                    elif message.data[0] == VU:
                        print('Auto, Close Cabin')
                    elif message.data[0] == VW: 
                        print('Auto, Open Cabin')
                    time.sleep(2) 


    except KeyboardInterrupt:
        exit()
    except Exception:
        traceback.print_exc(file=sys.stdout)
        exit()
    except OSError:
        exit()   
############################
# can0hvac
############################
if __name__ == "__main__":
    q                      = queue.Queue()
    rx                     = Thread(target = msgbuffer)
    cleanscreen()
    scroll()
    time.sleep(2)
    cleanscreen()
    scroll2()
    setup()
    rx.start()
    main()


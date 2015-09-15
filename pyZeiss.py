import serial
import time

def connect(port='com1'):
    s = serial.Serial(port, baudrate=57600, timeout=1)
    return s


def executeCmd(ser, command, targetDevice):
   # Prepare command according to CAN29 Protocol
   preparedCommand = 4*[None]
   preparedCommand[0] = 0x10
   preparedCommand[1] = 0x02
   preparedCommand[2] = targetDevice
   preparedCommand[3] = 0x11
   # copy command into preparedCommand, but double 0x10
   tenCounter = 0;
   for c in command:
      preparedCommand.append(c)
      if (c==0x10):
         preparedCommand.append(c)

      if (c==0x0D):
         preparedCommand.append(0x10)
         preparedCommand.append(c)

   preparedCommand.append(0x10)
   preparedCommand.append(0x03)

   # send command
   ser.write(''.join(map(chr, preparedCommand)))


def getAnswer(ser):
    etx = False # end of text
    timeout = False
    dle = False # data link escape
    answer = []

    while (not etx) and (not timeout):
        c = ser.read()
        if c == '':
            timeout = True
        elif dle:
            if ord(c) == 0x02:
                # Start of text.
                pass
            elif ord(c) == 0x03:
                # End of text.
                etx = True
            elif ord(c) == 0x10:
                # 0x10 is data.
                answer.append(c)
            elif ord(c) == 0x0d:
                # 0x0d is data.
                answer.append(c)
            else:
                raise Exception('Unexpected escaped character.')
            dle = False
        elif ord(c) == 0x10: # and not dle implicit
            dle = True
        else:
            answer.append(c)
    sourceAddress = answer[1:3]
    targetAddress = answer[-3:-1]
    return(answer, sourceAddress, targetAddress, timeout)


def monitor(ser):
    while True:
        resp = getAnswer(ser)
        if resp[-1]:
            # timeout
            time.sleep(1)
        else:
            print resp[0]

import utime
from machine import Pin

# set up data0 and data1 pins
data0_pin = Pin(0, Pin.IN, Pin.PULL_UP)
data1_pin = Pin(1, Pin.IN, Pin.PULL_UP)

# define constants for Wiegand protocol
WIEGAND_WAIT_TIME = 25
WIEGAND_LENGTH = 32

def read_wiegand():
    """
    Read RFID tag value using Wiegand protocol.
    """
    data = bytearray(WIEGAND_LENGTH//8)
    bit_count = 0
    
    while True:
        bit_0 = data0_pin.value()
        bit_1 = data1_pin.value()
        
        # wait for signal change or timeout
        if bit_0 == 0 or bit_1 == 0:
            utime.sleep_us(WIEGAND_WAIT_TIME)
            bit_0 = data0_pin.value()
            bit_1 = data1_pin.value()
            bit_count += 1
            
            # check if all bits have been read
            if bit_count == WIEGAND_LENGTH:
                return data
                
            # store the bit
            if bit_0 == 0 and bit_1 == 1:
                byte_index = (bit_count-1) // 8
                bit_index = (bit_count-1) % 8
                data[byte_index] |= 1 << bit_index
        else:
            # reset bit count
            bit_count = 0
            
def main():
    while True:
        # read RFID tag value
        rfid_data = read_wiegand()
        rfid_hex = ''.join('{:02X}'.format(x) for x in rfid_data)
        print("RFID tag value:", rfid_hex)

if __name__ == '__main__':
    main()

##Getting output like
##RFID tag value: F33C9E67
##RFID tag value: F33C8F63

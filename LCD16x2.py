from gpiozero import OutputDevice
from time import sleep

# GPIO port connections
LCD_RS = OutputDevice(25) #GPIO25 connected to RS
LCD_E = OutputDevice(24) #GPIO24 connected to Enable
LCD_D4 = OutputDevice(23) #GPIO24 connected to D4
LCD_D5 = OutputDevice(18) #GPIO18 connected to D5
LCD_D6 = OutputDevice(15) #GPIO15 connected to D6
LCD_D7 = OutputDevice(14) #GPIO14 connected to D7

# LCD parameters
LCD_WIDTH = 16  #Max characters per 16
LCD_CHR = True #Mode - Sending Data
LCD_CMD = False #Mode - Sending command
LCD_LINE_1 = 0x80 #LCD RAM address for 1st line
LCD_LINE_2 = 0xC0 #LCD RAM address for 2nd Line

#Timeing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

def lcd_toggle_enable():
    #Toogle enable pin
    sleep(E_DELAY)
    LCD_E.on()
    sleep(E_PULSE)
    LCD_E.off()
    sleep(E_DELAY)

def lcd_byte(bits, mode):
    #Send byte to data pins"
    #Send mode (true for data, false for command)
    LCD_RS.value = mode

    #Send High nibble (bits 7-4)
    LCD_D4.value = bool(bits & 0x10)
    LCD_D5.value = bool(bits & 0x20)
    LCD_D6.value = bool(bits & 0x40)
    LCD_D7.value = bool(bits & 0x80)
    lcd_toggle_enable()

    #Send Low nibble (bits 3-0)
    LCD_D4.value = bool(bits & 0x01)
    LCD_D5.value = bool(bits & 0x02)
    LCD_D6.value = bool(bits & 0x04)
    LCD_D7.value = bool(bits & 0x08)
    lcd_toggle_enable()
    
def lcd_init():
    #LCD display Initialization
    lcd_byte(0x33, LCD_CMD) #Initialize
    lcd_byte(0x32, LCD_CMD) #Initialize
    lcd_byte(0x28, LCD_CMD) #2 Line 5x7 matrix
    lcd_byte(0x0C, LCD_CMD) #Turn cursor off
    lcd_byte(0x06, LCD_CMD) #Shift cursor right
    lcd_byte(0x01, LCD_CMD) #Clear display
    sleep(E_DELAY)

def lcd_string(message, line):
    # Send string to display
    message = message.ljust(LCD_WIDTH, " ")

    lcd_byte(line, LCD_CMD)

    for char in message:
        lcd_byte(ord(char), LCD_CHR)
        
# Main
if __name__ == '__main__':
    lcd_init()
    while True:
        lcd_string("Hello", LCD_LINE_1)
        lcd_string("Testing", LCD_LINE_2)
        sleep(3)
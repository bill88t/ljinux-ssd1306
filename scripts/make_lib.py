from platform import uname
from os import listdir, system


def errexit():
    print("Compilation error, exiting")
    exit(1)


mpyn = "./scripts/mpy-cross-" + uname().machine

print(f"Compiling adafruit_ssd1306 and adafruit_framebuf..\nUsing mpycross: {mpyn}\n")

a = system(
    mpyn
    + " ./submodules/Adafruit_CircuitPython_framebuf/adafruit_framebuf.py -s adafruit_framebuf -v -O4 -o ./files/adafruit_framebuf.mpy"
)
print("adafruit_framebuf.py -> adafruit_framebuf.mpy")

if a != 0:
    errexit()

a = system(
    mpyn
    + " ./submodules/Adafruit_CircuitPython_SSD1306/adafruit_ssd1306.py -s adafruit_ssd1306 -v -O4 -o ./files/adafruit_ssd1306.mpy"
)
print("adafruit_ssd1306.py -> adafruit_ssd1306.mpy")

if a != 0:
    errexit()

print("Compiling ljinux-ssd1306 driver..\n")

a = system(
    mpyn
    + " ./resources/display-ssd1306.py -s ljinux-ssd1306 -v -O4 -o ./files/ssd1306.mpy"
)
print("display-ssd1306.py -> ssd1306.mpy")

if a != 0:
    errexit()

print()

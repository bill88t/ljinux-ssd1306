ljinux.api.setvar("argj", "cp ssd1306.mpy &/lib/drivers/ssd1306.mpy")
ljinux.based.command.fpexec("/bin/cp.py")

ljinux.api.setvar("argj", "cp adafruit_ssd1306.mpy &/lib/adafruit_ssd1306.mpy")
ljinux.based.command.fpexec("/bin/cp.py")

ljinux.api.setvar("return", "0")

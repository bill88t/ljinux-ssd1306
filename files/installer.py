ljinux.api.var("argj", f"cp display.lja /bin/display.lja")
ljinux.based.command.fpexecc([None, "/bin/cp.py"])
ljinux.api.var("argj", f"cp display.py /bin/display.py")
ljinux.based.command.fpexecc([None, "/bin/cp.py"])
ljinux.api.var("argj", f"cp ssd1306.mpy &/lib/drivers/ssd1306.mpy")
ljinux.based.command.fpexecc([None, "/bin/cp.py"])
ljinux.api.var("argj", f"cp font5x8.bin &/font5x8.bin")
ljinux.based.command.fpexecc([None, "/bin/cp.py"])

for filee in [
    "adafruit_framebuf.mpy",
    "adafruit_ssd1306.mpy",
]:
    ljinux.api.var("argj", f"cp {filee} &/lib/{filee}")
    ljinux.based.command.fpexecc([None, "/bin/cp.py"])

ljinux.api.var("return", "0")

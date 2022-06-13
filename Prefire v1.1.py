from os import system, _exit

system("mode 80,18 & title Prefire v1.1 & powershell $H=get-host;$W=$H.ui.rawui;$B=$W.buffersize;$B.width=80;$B.height=9999;$W.buffersize=$B;")

from time import sleep, perf_counter
from ctypes import WinDLL

print('''\033[32mPrefire \033[37mv1.1 made by \033[32mqurex \033[37mand \033[32malt
''')



def exit_():
    system("echo Press any key to exit . . . & pause >nul")
    _exit(0)


ERROR = "\x1b[38;5;255m[\x1b[31m-\x1b[38;5;255m]"
SUCCESS = "\x1b[38;5;255m[\x1b[32m+\x1b[38;5;255m]"
INFO = "\x1b[38;5;255m[\x1b[35m*\x1b[38;5;255m]"


try:
    from PIL.Image import frombytes
    from mss import mss
    from keyboard import is_pressed, add_hotkey, block_key, unblock_key
except ModuleNotFoundError:
    print(f"{INFO} Installing required modules.")
    o = system("pip3 install keyboard mss pillow --quiet --no-warn-script-location --disable-pip-version-check")


try:
    TRIGGER, HIGHLIGHT = [line.strip() for line in open("config.txt")]
    print(f"{SUCCESS} Hotkey: {TRIGGER}\n{SUCCESS} Enemy highlight colour: {HIGHLIGHT}\n")
except (FileNotFoundError, ValueError):
    print(f"{ERROR} Missing or invalid config.txt\n")
    HIGHLIGHT = input(f"{INFO} Choose your enemy colour:\n\n[\x1b[35m1\x1b[38;5;255m] red \n[\x1b[35m2\x1b[38;5;255m] purple\n[\x1b[35m3\x1b[38;5;255m] yellow\n\n> ")
    if HIGHLIGHT not in ["1", "2", "3"]:
        print(f"{ERROR} Choose 1, 2 or 3 retard.\n")
        exit_()
    if HIGHLIGHT == "1":
        HIGHLIGHT = "red"
    elif HIGHLIGHT == "2":
        HIGHLIGHT = "purple"
    elif HIGHLIGHT == "3":
        HIGHLIGHT = "yellow"
    print(f"\n{SUCCESS} Wrote enemy highlight colour to config.txt\n{INFO} Now write your hotkey in config.txt\n")
    with open("config.txt", "w") as f:
        f.write(f"Replace this first line with your hotkey.  e.g.  c   or   `   or even   ctrl + alt + z\n{HIGHLIGHT}")
    exit_()


if HIGHLIGHT == "red":
    R, G, B = (152, 20, 37)
elif HIGHLIGHT == "purple":
    R, G, B = (250, 100, 250)
elif HIGHLIGHT == "yellow":
    R, G, B = (252, 252, 84)                         #added yellow RGB

MODE = input(f"{INFO} Mode\n\n[\x1b[35m1\x1b[38;5;255m] Hold\n[\x1b[35m2\x1b[38;5;255m] Toggle\n\n> ")
if MODE not in ["1", "2"]:
    print(f"{ERROR} Choose 1 or 2 retard.\n")
    exit_()


user32, kernel32, shcore = WinDLL("user32", use_last_error=True), WinDLL("kernel32", use_last_error=True), WinDLL("shcore", use_last_error=True)

shcore.SetProcessDpiAwareness(2)
WIDTH, HEIGHT = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

TOLERANCE, ZONE = 20, 5
GRAB_ZONE = (int(WIDTH / 2 - ZONE), int(HEIGHT / 2 - ZONE), int(WIDTH / 2 + ZONE), int(HEIGHT / 2 + ZONE))


class PopOff:
    def __init__(self):
        self.active = False
        kernel32.Beep(440, 75), kernel32.Beep(200, 100)

    def switch(self):
        self.active = not self.active
        kernel32.Beep(440, 75), kernel32.Beep(700, 100) if self.active else kernel32.Beep(440, 75), kernel32.Beep(200, 100)

    def search(self):
        start_time = perf_counter()
        with mss() as sct:
            img = sct.grab(GRAB_ZONE)
        pmap = frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
        for x in range(0, ZONE * 2):
            for y in range(0, ZONE * 2):
                r, g, b = pmap.getpixel((x, y))
                if R - TOLERANCE < r < R + TOLERANCE and G - TOLERANCE < g < G + TOLERANCE and B - TOLERANCE < b < B + TOLERANCE:
                    print(f"\x1b[2A{SUCCESS} Reaction time: {int((perf_counter() - start_time) * 1000)}ms")
                    blocked, held = [], []
                    if any(user32.GetKeyState(k) > 1 for k in [87, 65, 83, 68]):
                        if is_pressed("a"):
                            block_key(30)
                            blocked.append(30)
                            user32.keybd_event(68, 0, 0, 0)
                            held.append(68)
                        if is_pressed("d"):
                            block_key(32)
                            blocked.append(32)
                            user32.keybd_event(65, 0, 0, 0)
                            held.append(65)
                        if is_pressed("w"):
                            block_key(17)
                            blocked.append(17)
                            user32.keybd_event(83, 0, 0, 0)
                            held.append(83)
                        if is_pressed("s"):
                            block_key(31)
                            blocked.append(31)
                            user32.keybd_event(87, 0, 0, 0)
                            held.append(87)
                        sleep(0.1)
                    user32.mouse_event(2, 0, 0, 0, 0)
                    sleep(0.005)
                    user32.mouse_event(4, 0, 0, 0, 0)
                    for b in blocked:
                        unblock_key(b)
                    for h in held:
                        user32.keybd_event(h, 0, 2, 0)
                    break

    def hold(self):
        while 1:
            if is_pressed(TRIGGER):
                while is_pressed(TRIGGER):
                    self.search()
            else:
                sleep(0.1)

    def toggle(self):
        add_hotkey(TRIGGER, self.switch)
        while 1:
            self.search() if self.active else sleep(0.5)


o = system("cls")
if MODE == "1":
    PopOff().hold()
elif MODE == "2":
    PopOff().toggle()
#858dc15665e31669d0ca7117fe14ecc2
#f21fcc937920b76ed421d66f8950a669
#5be97e6d484baae0602dab9f644d11cd
#6721cc13199a2cb4b0efd1a7e118a3eb
#cee4ea90ca3a09035bcab12846d1a6fc
#6f7ab00610358c9e0bb7c0aa68950455
#f7fbf317a7ce8f3edb4a01ada90184db
#1b9edd0ea6b5ec06eef61b96b24cb13b
#117473f180ffeafdf408031c5d50f2f3
#3c3da3ab14e05c0978392392e260a175
#9c8573c4e97a59ca15e60ab861928420
#e1bf3cbb9ab714ff9ab9a3a77972f58c
#cab61b8be7f35bfd92a05e492a6d083c
#d9db5b79f9fe805745c7406ab3778bec
#123993b5fb74f31fa9c2bd419d8380b0
#808ee6715c2b1037c3c12de72447cd3d
#117b3408412e72ddc5147dad287c8bb4
#220378b3eb8a353e551f79cb98dd684e
#610e724a23e6803b535c1322f6bd8e34
#7d646433479fbefd75520f68ded532e4
#8a6e64bcfa657f3ab283ab9fbe004342
#fc8f19adec32efa08b26fb11001e0102
#f7436acfcc38df4d252a6b2b94882153
#7ff806090db0c07dcad8f8c4cc46ad95
#c57b6d788dd145fcce39dd35724c6ce9
#bbc1322d327144c37d161a05751e75f1
#d5a74a2dea93496dccce347136db316c
#b0e7f769f257dc3929bfbb703ed9ec8f
#3c6b6a6c88ff6265bfff39f37d3c25f3
#feea11391b8135227f9af0e384237b78
#1c70cc2625e2f0369de2dee6b647e194
#4794b858a4440eb97481b63d48df3d52
#bd852a8c09e9451c75b121796277a630
#22661f1b77aaea87b017aa9e88aca860
#dd0af891bcfefca0e58ad8ba3746d3fa
#050e762ff0f50f0d8c135c1825fb0547
#e359716defdb6f24fc0e7725a62e18f4
#95113e084cd4eba1583f206aabad2c51
#37642987bff070a35dc1256a5ad37c6e
#c8715315982e227dcb26040b2fdee69a
#c53b5664465e95c210b6bcc1597f9685
#4d254f65aa3d28417ae7a80cb8613f25
#aee5df7ed0fb4b7db50d074f32622f6f
#54a9a827c05da35b52a158983aa81d20
#33c2c011ba3fde9ca56ae38a63fddc63
#a684fee8cefa9296a5c9ddc76e323d93
#64d43f3316bf8ee335343ed702320a9d
#7790f40bea8e7c2d7fb808b1c345da8f
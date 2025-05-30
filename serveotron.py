import os
import time
import sys
import logging
import json
from colorama import init, Fore as fore
from typing import List, Dict
import subprocess
import platform

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('serveotron.log'),
        logging.StreamHandler()
    ]
)

class Serveotron:
    def __init__(self):
        self.config_file = 'config.json'
        self.default_config = {
            'servers': {
                'serveo': {
                    'host': 'serveo.net',
                    'ip': '138.68.79.95'
                }
            },
            'default_server': 'serveo'
        }
        self.load_config()
        init()

    def load_config(self):
        """Load or create configuration file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = self.default_config
                self.save_config()
        except Exception as e:
            logging.error(f"Error loading configuration: {e}")
            self.config = self.default_config

    def save_config(self):
        """Save configurations to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving configuration: {e}")

    def check_dependencies(self) -> bool:
        """Check if all dependencies are installed"""
        try:
            import colorama
            return True
        except ImportError:
            print(f"{fore.RED}Error: colorama is not installed. Installing...{fore.RESET}")
            subprocess.run([sys.executable, "-m", "pip", "install", "colorama"])
            return True

    def banner(self):
        """Display program banner"""
        print(f"""
   {fore.WHITE}___   I'M SERVEOTRON!!!
 /| {fore.RED}O{fore.WHITE} |\\   
(  \\_/  ) 
 \\     /     
  |   |         {fore.CYAN}CODED BY BR3NO🐍{fore.WHITE} >>> https://github.com/Br3noAraujo
  {fore.RED}0   0 {fore.RESET}""")
        print(f"\n{fore.GREEN}Version 2.0 - SSH Tunnel Server{fore.RESET}")

    def read_ports(self) -> List[str]:
        """Read ports from ports.txt file"""
        try:
            if not os.path.exists('ports.txt'):
                print(f"{fore.YELLOW}ports.txt file not found. Creating...{fore.RESET}")
                with open('ports.txt', 'w') as f:
                    f.write("80\n443\n8080")
                return ["80", "443", "8080"]
            
            with open('ports.txt', 'r') as f:
                ports = [port.strip() for port in f.readlines() if port.strip()]
            return ports
        except Exception as e:
            logging.error(f"Error reading ports: {e}")
            return []

    def create_tunnel_command(self, ports: List[str], server: str) -> str:
        """Create SSH tunnel command"""
        string = ''
        for port in ports:
            string += f'-R {port}:localhost:{port} '
        return f'ssh {string} {server}'

    def show_menu(self):
        """Display main menu"""
        while True:
            print(f"\n{fore.CYAN}=== MAIN MENU ==={fore.RESET}")
            print("1. Start tunnels")
            print("2. Configure servers")
            print("3. Check status")
            print("4. Exit")
            
            choice = input(f"\n{fore.GREEN}Choose an option: {fore.RESET}")
            
            if choice == "1":
                self.start_tunnels()
            elif choice == "2":
                self.configure_servers()
            elif choice == "3":
                self.check_status()
            elif choice == "4":
                print(f"\n{fore.YELLOW}Exiting...{fore.RESET}")
                break
            else:
                print(f"{fore.RED}Invalid option!{fore.RESET}")

    def start_tunnels(self):
        """Start SSH tunnels"""
        ports = self.read_ports()
        if not ports:
            print(f"{fore.RED}No ports configured!{fore.RESET}")
            return

        server = self.config['servers'][self.config['default_server']]
        print(f"\n{fore.GREEN}Starting tunnels to {server['host']}...{fore.RESET}")
        print(f"Ports: {', '.join(ports)}")
        
        try:
            command = self.create_tunnel_command(ports, server['host'])
            logging.info(f"Executing command: {command}")
            os.system(command)
        except Exception as e:
            logging.error(f"Error starting tunnels: {e}")
            print(f"{fore.RED}Error starting tunnels: {e}{fore.RESET}")

    def configure_servers(self):
        """Configure available servers"""
        print(f"\n{fore.CYAN}=== SERVER CONFIGURATION ==={fore.RESET}")
        for name, server in self.config['servers'].items():
            print(f"\nServer: {name}")
            print(f"Host: {server['host']}")
            print(f"IP: {server['ip']}")
        
        choice = input(f"\n{fore.GREEN}Enter default server name: {fore.RESET}")
        if choice in self.config['servers']:
            self.config['default_server'] = choice
            self.save_config()
            print(f"{fore.GREEN}Default server updated!{fore.RESET}")
        else:
            print(f"{fore.RED}Server not found!{fore.RESET}")

    def check_status(self):
        """Check tunnel status"""
        print(f"\n{fore.CYAN}=== SYSTEM STATUS ==={fore.RESET}")
        print(f"Operating System: {platform.system()} {platform.release()}")
        print(f"Python: {platform.python_version()}")
        print(f"Default Server: {self.config['default_server']}")
        
        ports = self.read_ports()
        print(f"\nConfigured Ports: {len(ports)}")
        for port in ports:
            print(f"- {port}")

def main():
    serveotron = Serveotron()
    if serveotron.check_dependencies():
        serveotron.banner()
        serveotron.show_menu()

if __name__ == "__main__":
    main()

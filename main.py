import os
import time
from colorama import init, Fore as fore # ___
init()  #  <<<<-----------------------------|
def banner():
    print(f"""
   {fore.WHITE}___   I'M SERVEOTRON!!!
 /| {fore.RED}O{fore.WHITE} |\\   
(  \\_/  ) 
 \\     /     
  |   |         {fore.CYAN}CODED BY BR3NO🐍{fore.WHITE} >>> https://github.com/Br3noAraujo
  {fore.RED}0   0 {fore.RESET}""")
    
def main():
    banner()
    ports = open('ports.txt', '+r')
    ports = ports.readlines()
    print('\n')
    string = ''
    for port in ports:
        port = port.replace('\n', '')
        string = string + (f'-R {port}:localhost:{port} ')
    print(f'SERVEO.NET   = 138.68.79.95')   
    os.system(f'ssh {string} serveo.net')

if __name__ ==  "__main__":
    main()
from socket import *
import time

meuHost = '127.0.0.1'
minhaPorta = 5000

sockobj = socket(AF_INET, SOCK_DGRAM)
dest = (meuHost, minhaPorta)

print('Para sair use CTRL+X\n')
msg = "a"
while True:
    sockobj.sendto(msg.encode(), dest)
    time.sleep(1)

sockobj.close()
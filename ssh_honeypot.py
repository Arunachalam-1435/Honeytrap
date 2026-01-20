#libraries
import logging
from logging.handlers import RotatingFileHandler
import socket
import paramiko

#constants
format = logging.Formatter('%(message)s')

#loggers
logger = logging.getLogger("FunnelLogger")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('audit.log',maxBytes=2000, backupCount=5)
handler.setFormatter(format)
logger.addHandler(handler)

cmd_logger = logging.getLogger("FunnelLogger")
cmd_logger.setLevel(logging.INFO)
cmd_handler = RotatingFileHandler('cmd_audit.log',maxBytes=2000, backupCount=5)
cmd_handler.setFormatter(format)
cmd_logger.addHandler(cmd_handler)

#shell emulation
def shell_emulator(channel, client_ip):
    channel.send(b'ubuntu-vm$ ')
    cmd = b""
    while True:
        char = channel.recv(1)
        channel.send(char)
        if not char:
            channel.close()
        cmd += char
        if char == b'\r':
            if cmd.strip() == b'exit':
                response = b'\n Goodbye\n'
                channel.close()
            elif cmd.strip() == b'pwd':
                response = b"\n" + b'\\usr\\local' + b'\r\n'
            elif cmd.strip() == b'whoami':
                response = b"\n" + b"user1" + b"\r\n"
            elif cmd.strip() == b'ls':
                response = b'\n' + b"sys.conf" + b"\r\n"
            elif cmd.strip() == b'cat sys.conf':
                response = b'\n' + b"Welcome to our server!" + b"\r\n"
            else:
                response = b"\n" + bytes(cmd.strip()) + b"\r\n"
        channel.send(response)
        channel.send(b'ubuntu-vm$ ')
        cmd = b""
# SSH server
class Server(paramiko.ServerInterface):
    def __init__(self, client_ip, username=None, password=None):
        self.client_ip = client_ip
        self.username = username
        self.password = password
    
    def check_channel_req(self, kind: str, chanid: int) -> int:
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
    def get_allowed_auth(self):
        return "password"
    def check_auth_password(self, username, password):
        if self.username is not None and self.password is not None:
            if username == 'username' and password == 'password':
                return paramiko.AUTH_SUCCESSFUL
            else:
                return paramiko.AUTH_FAILED
    def check_channel_shell_req(self, channel):
        self.event.set()
        return True
    def check_channel_pty_req(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True
    def check_channel_exec_req(self, channel, command) -> bool:
        command = str(command)
        return True
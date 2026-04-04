#libraries
import logging
from logging.handlers import RotatingFileHandler
import socket
import paramiko
import threading

#constants
format = logging.Formatter('%(message)s')
SSH_BANNER = "SSH-2.0-MySSHServer_1.0"
#host_key = 'server.key'
host_key = paramiko.RSAKey(filename='server.key')
#loggers
logger = logging.getLogger("FunnelLogger")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('audit.log',maxBytes=2000, backupCount=5)
handler.setFormatter(format)
logger.addHandler(handler)

creds_logger = logging.getLogger("CredsLogger")
creds_logger.setLevel(logging.INFO)
creds_handler = RotatingFileHandler('cmd_audit.log',maxBytes=2000, backupCount=5)
creds_handler.setFormatter(format)
creds_logger.addHandler(creds_handler)

#shell emulation
def shell_emulator(channel, client_ip): 
    channel.send(b'ubuntu-vm$ ') 
    cmd = b"" 
    while True: 
        char = channel.recv(1) 
        channel.send(char) 
        if not char: 
            channel.close()
            break 
        cmd += char 
        if char == b'\r': 
            if cmd.strip() == b'exit': 
                response = b'\n Goodbye\n' 
                channel.close() 
            elif cmd.strip() == b'pwd': 
                response = b"\n" + b'\\usr\\local' + b'\r\n' 
                creds_logger.info(f"command {cmd.strip()} executed by {client_ip}")
            elif cmd.strip() == b'whoami': 
                response = b"\n" + b"user1" + b"\r\n" 
                creds_logger.info(f"command {cmd.strip()} executed by {client_ip}")
            elif cmd.strip() == b'ls': 
                response = b'\n' + b"sys.conf" + b"\r\n" 
                creds_logger.info(f"command {cmd.strip()} executed by {client_ip}")
            elif cmd.strip() == b'cat sys.conf': 
                response = b'\n' + b"Welcome to our server!" + b"\r\n"
                creds_logger.info(f"command {cmd.strip()} executed by {client_ip}") 
            else: 
                response = b"\n" + bytes(cmd.strip()) + b"\r\n" 
                creds_logger.info(f"command {cmd.strip()} executed by {client_ip}")
            channel.send(response) 
            channel.send(b'ubuntu-vm$ ') 
            cmd = b""

# SSH server
class Server(paramiko.ServerInterface): 
    def __init__(self, client_ip, username=None, password=None): 
        self.event = threading.Event() 
        self.client_ip = client_ip 
        self.username = username 
        self.password = password 
    def check_channel_request(self, kind: str, chanid: int) -> int: 
        if kind == 'session': 
            return paramiko.OPEN_SUCCEEDED 
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def get_allowed_auth(self): 
        return "password" 
    def check_auth_password(self, username, password): 
        logger.info(f"Client {self.client_ip} attempted connection with username: {username} and password: {password}")
        creds_logger.info(f"{self.client_ip}, {username}, {password}")
        if self.username is not None and self.password is not None: 
            if username == self.username and password == self.password: 
                return paramiko.AUTH_SUCCESSFUL 
            else: return paramiko.AUTH_FAILED 
        else: 
            return paramiko.AUTH_SUCCESSFUL 
    def check_channel_shell_request(self, channel): 
        self.event.set() 
        return True 
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes): 
        return True 
    def check_channel_exec_request(self, channel, command) -> bool: 
        command = str(command) 
        return True

def client_handle(client, address, username, password): 
    client_ip = address[0] 
    print(f"{client_ip} has connected to the server.") 
    try: 
        transport = paramiko.Transport(client) 
        transport.local_version = SSH_BANNER 
        server = Server(client_ip=client_ip, username=username, password=password) 
        transport.add_server_key(host_key) 
        transport.start_server(server=server) 
        
        channel = transport.accept(10)
        if channel is None: 
            print("No channel was opened.") 
            return
        server.event.wait(10)
        if not server.event.is_set():
            print("Client never asked for a shell.") 
            return
        standard_banner = "Welcome to Ubuntu 22.04 LTS!\r\n\r\n" 
        channel.send(standard_banner) 
        
        shell_emulator(channel, client_ip=client_ip) 
    except Exception as error: 
        print(error) 
        print("!!! ERROR !!!") 
    finally: 
        try: 
            transport.close() 
        except Exception as error: 
            print(error) 
            print("!!! ERROR !!!") 
        client.close()
        
# Provision SSH-based Honeypot
def honeypot(address, port, username, password): 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    sock.bind((address, port)) 
    sock.listen(10) 
    print(f"SSH server is listening on port: {port}.") 
    while True: 
        try: 
            client, addr = sock.accept() 
            ssh_honeypot_thread = threading.Thread(target=client_handle, args=(client, addr, username, password))
            ssh_honeypot_thread.start() 
        except Exception as error: 
            print(error)
honeypot('127.0.0.1', 2222, 'username', 'password')
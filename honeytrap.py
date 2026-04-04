import argparse
from ssh_honeypot import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", type=str, required=True)
    parser.add_argument("-p", "--port", type=int, required=True)
    parser.add_argument("-u", "--username", type=str)
    parser.add_argument("-pw", "--password", type=str)

    parser.add_argument("-s", "--ssh", action="store_true")
    parser.add_argument("-w", "--web", action="store_true")

    args = parser.parse_args()

    try:
        if args.ssh:
            print("SSH honeypot selected")
            honeypot(args.address, args.port, args.username, args.password)
            if not args.username:
                username = "username"
            if not args.password:
                password = "password"    
        elif args.web:
            print("Web based honeypot selected")
            pass
        else:
            print("Choose a right honeypot. --ssh for SSH and --web for web based one")
    except Exception as error:
        print("\n Exiting Honeytrap Honeypot application...\n")
# import libraries
import argparse
from ssh_honeypot import *
from web_honeypot import *

#main logic
if __name__ == "__main__":
    # add cmd arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", type=str, required=True)
    parser.add_argument("-p", "--port", type=int, required=True)
    parser.add_argument("-u", "--username", type=str, default=None)
    parser.add_argument("-pw", "--password", type=str, default=None)

    parser.add_argument("--ssh", action="store_true")
    parser.add_argument("--web", action="store_true")

    args = parser.parse_args()

    try:
        # choose SSH honeypot
        if args.ssh:
            print("SSH honeypot selected")
            if args.username is None:
                args.username = "username"
            if args.password is None:
                args.password = "password"
            honeypot(args.address, args.port, args.username, args.password)
        # choose web honeypot    
        elif args.web:
            print("Web based honeypot selected")
            if args.username is None:
                args.username = "admin"
            if args.password is None:
                args.password = "password"
            run_web_honeypot(args.port, args.username, args.password)
        else:
            print("Choose a right honeypot. --ssh for SSH and --web for web based one")
    except Exception as error:
        print("\n Exiting Honeytrap Honeypot application...\n")
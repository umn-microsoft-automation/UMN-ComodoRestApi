import requests, argparse, comodo, sys

parser = argparse.ArgumentParser(description="Get InCommon Certs")
parser.add_argument("--login", required=True, help="")
parser.add_argument("--pswd", required=True, help="")
parser.add_argument("--proxy", help="Proxy address, assumes https")
#parser.add_argument("--", required=True, help="")
args = parser.parse_args()

header = {'login':args.login,'password':args.pswd,'customerUri':'InCommon','Content-Type':'application/json'}
if args.proxy:
    extras = {'proxies':{'https':args.proxy}}
    data = extras

list = comodo.getlist(header,**data)
print (list)

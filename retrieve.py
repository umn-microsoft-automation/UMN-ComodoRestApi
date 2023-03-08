import requests, subprocess, argparse, make_openssl_config, comodo, sys, json, pprint, time
from shutil import copyfile

parser = argparse.ArgumentParser(description="Get InCommon Certs")
parser.add_argument("--cn", required=True, help="CommonName")
parser.add_argument("--login", required=True, help="")
parser.add_argument("--pswd", required=True, help="")
parser.add_argument("--sslId", required=True, help="sslId provided during Enroll phase")

#http://docs.python-requests.org/en/master/api/
#parser.add_argument("--", required=True, help="")
args = parser.parse_args()


## wait/check for completion, currently no way to check with API
loop = 0
downloaded = False
while True:
	try:
		loop += 1
		if loop > 10:
			break
		time.sleep(40)
		header2 = {'login':args.login,'password':args.pswd,'customerUri':'InCommon'}
		sslId = args.sslId
		ref = comodo.retrieve(str(sslId),'base64',header2,**extras)
		with open(args.cn+'.p7b', 'wb') as f:
				for chunk in ref.iter_content(chunk_size=1024): 
					if chunk: # filter out keep-alive new chunks
						f.write(chunk)
		downloaded = True
		break
	except:
		print('keep checking')
if downloaded != True:
	sys.exit("Failed to retrieve cert from commodo after 200 secondsd")

# Convert the pkcs7 binary file into x509 certs or pfx
subprocess.check_call(['openssl', 'pkcs7','-print_certs', '-in',  args.cn+'.p7b', '-out', args.cn+'.cer'])
if args.platform == 'windows':
	subprocess.check_call(['openssl', 'pkcs12','-export', '-in',  args.cn+'.cer', '-inkey', args.cn+'.key', '-out', args.cn+'.pfx', '-password',  'pass:'+args.certPSWD])
	
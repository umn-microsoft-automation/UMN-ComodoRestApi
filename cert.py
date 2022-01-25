import requests, subprocess, argparse, make_openssl_config, comodo, sys, json, pprint, time


'''
https://enterprise.comodo.com/security-solutions/digital-certificates/certificate-manager/certificate-manager-support-docs/incommon-docs/rest-api-doc.html
'''


parser = argparse.ArgumentParser(description="Get InCommon Certs")
parser.add_argument("--unitName", required=True, help="Unit Short ID")
parser.add_argument("--cn", required=True, help="CommonName")
parser.add_argument("--email", required=True, help="EmailAddress")
parser.add_argument("--login", required=True, help="")
parser.add_argument("--pswd", required=True, help="")
parser.add_argument("--certPSWD", required=True, help="Secret Key")
parser.add_argument("--platform", required=True, help="windows or linux")
parser.add_argument("--altNames", help="Comma-Separated list of DNS Subject Alternative Names (SANs), limit 100")
parser.add_argument("--orgId", required=True, help="Your Org ID")
parser.add_argument("--reqOps", help="Request options to be passed into requests.request **kwargs")
#http://docs.python-requests.org/en/master/api/
#parser.add_argument("--", required=True, help="")
args = parser.parse_args()

''

# Generate the CSR and private key locally
print( 'Generating CSR and private key' )
# create .cnf file for CSR
make_openssl_config.openssl_config(args.cn,args.unitName,args.email,'University of MN',args.altNames)
# create Private Key
subprocess.check_call(['openssl', 'genrsa','-out', args.cn+'.key', '2048'])
# create csr
subprocess.check_call(['openssl', 'req', '-new', '-batch', '-key', args.cn+'.key', '-config', args.cn+'.cnf', '-out', args.cn+'.csr'])


# Create the public key on Comodo's end
with open(args.cn+'.csr', 'r') as f:
	csr = f.read()
print( 'Logging into Comodo' )

header = {'login':args.login,'password':args.pswd,'customerUri':'InCommon','Content-Type':'application/json'}
extras = args.reqOps
#pprint.pprint(comodo.getlist(header,**extras))

#use comodo.getlist to find
certID = 226
term = 365
if args.platform == 'windows':
	serverType = 14
else:
	serverType = 2
# create json request
reqjson = {'orgId':args.orgId,'csr':csr,'certType':certID,'numberServers':0,'serverType':serverType,'term':term,'comments':"supercomments"}
if args.altNames:
	reqjson['subjAltNames'] = args.altNames
data = extras
print(reqjson)
#sys.exit()
data['json'] = reqjson
# erroll cert and store in response
response  = comodo.enroll(header,**data)
#response = json.loads(jdata)
pprint.pprint(response)

## wait/check for completion, currently no way to check with API
loop = 0
downloaded = False
while True:
	try:
		loop += 1
		if loop > 10:
			break
		time.sleep(40)
		header2 = {'login':args.login,'password':args.pswd,'customerUri':'InCommon','stream':'True'}
		sslId = response['sslId']
		ref = comodo.retrieve(str(sslId),'base64',header,**extras)
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
	



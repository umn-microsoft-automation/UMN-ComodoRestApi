import requests, json
# https://enterprise.comodo.com/security-solutions/digital-certificates/certificate-manager/certificate-manager-support-docs/incommon-docs/rest-api-doc.html#resources-SSL

def basecall(path,header,method,**kwargs):
    url = "https://cert-manager.com/api/ssl/v1/" + path
    response = requests.request(method, url, headers=header,**kwargs)
    response.raise_for_status()
    return response

def getlist(header,**kwargs):
    data = basecall("types",header,'GET',**kwargs)
    return data.json()

def enroll(header,**kwargs):
    data = basecall("enroll",header,'POST',**kwargs)
    return data.json()

def retrieve(sslID,formatType,header,**kwargs):
    data = basecall("collect/"+sslID+"/"+formatType,header,'GET',**kwargs)
    return data

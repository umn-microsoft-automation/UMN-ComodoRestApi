"""
Script to generate an OpenSSL config file. See man page `config(5ssl)` for
details on the OpenSSL config file format.
"""

import sys
from configparser import ConfigParser
from collections import OrderedDict

def openssl_config(cn,unitName,email,orgName,altNames=None):
    """Generate a ConfigParser object containing all the OpenSSL configuration entries."""
    config = ConfigParser()

    # override option that makes all keys lowercase
    config.optionxform = lambda x: x

    config['req'] = OrderedDict()
    config['req']['string_mask'] = 'nombstr'
    config['req']['prompt'] = 'yes'
    config['req']['default_bits'] = '2048'
    config['req']['distinguished_name'] = 'req_distinguished_name'
    config['req']['attributes'] = 'req_attributes'
    config['req']['default_md'] = 'sha256'

    config['req_attributes'] = {}

    config['req_distinguished_name'] = OrderedDict()
    config['req_distinguished_name']['countryName'] = 'Country Name (2 letter code)'
    config['req_distinguished_name']['countryName_default'] = 'US'
    config['req_distinguished_name']['countryName_min'] = '2'
    config['req_distinguished_name']['countryName_max'] = '2'
    config['req_distinguished_name']['stateOrProvinceName'] = 'State or Province Name (full name)'
    config['req_distinguished_name']['stateOrProvinceName_default'] = 'Minnesota'
    config['req_distinguished_name']['localityName'] = 'Locality Name (eg, city)'
    config['req_distinguished_name']['localityName_default'] = 'Minneapolis'
    config['req_distinguished_name']['0.organizationName'] = 'Organization Name (eg, company)'
    config['req_distinguished_name']['0.organizationName_default'] = orgName
    config['req_distinguished_name']['organizationalUnitName'] = 'Organizational Unit Name (eg, section)'
    config['req_distinguished_name']['organizationalUnitName_default'] = unitName
    config['req_distinguished_name']['commonName'] = 'Common Name (eg, hostname)'
    config['req_distinguished_name']['commonName_default'] = cn
    config['req_distinguished_name']['commonName_max'] = '64'
    config['req_distinguished_name']['emailAddress'] = 'Email Address'
    config['req_distinguished_name']['emailAddress_max'] = '40'
    config['req_distinguished_name']['emailAddress_default'] = email

    if altNames:
            config['req']['req_extensions'] = "req_ext"
            config['req_ext'] = OrderedDict()
            # custruct string
            an = ''
            for i in altNames.split(","):
                temp = 'DNS:' + i + ','
                an += temp
            an = an[:-1]
            config['req_ext']['subjectAltName'] =  an

    file = open(cn+'.cnf','w')
    config.write(file)
    file.close()
    return config

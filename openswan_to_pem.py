#!/usr/bin/python

from Crypto.PublicKey import RSA

comps = {}

with open('/etc/ipsec.secrets') as f:
    for line in f:
        line = line.split(':', 1)
        if len(line) == 2:
            k = line[0].strip()

            v = line[1].strip()
            if v.startswith('0s'):
                v = int(v[2:], 64)
            elif v.startswith('0x'):
                v = int(v[2:], 16)

            comps[k] = v

r = RSA.construct((comps['Modulus'], comps['PublicExponent'],
                   comps['PrivateExponent']))
print(r.exportKey('PEM').decode('ascii'))

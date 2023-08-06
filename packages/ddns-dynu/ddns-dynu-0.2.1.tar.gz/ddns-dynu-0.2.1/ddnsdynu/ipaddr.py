import netifaces
import requests
import re
from ddnsdynu import log

def get_ipv6(ifname):
    return netifaces.ifaddresses(ifname)[netifaces.AF_INET6][1]['addr']

def get_ipv4_addr():
    try:
        session = requests.session()
        session.trust_env = False
        response = session.get('http://cip.cc',headers={
            'User-Agent': 'curl/7.68.0',
            'Accept-Encoding': '*'})
        buf = response.content.decode()
        ipv4 = buf.split('\n')[0][5:]
        if len(re.findall(r'\d+\.\d+\.\d+\.\d+', ipv4)) > 0:
            log.info("public ipv4 addr %s" % ipv4)
            return ipv4
        else:
            return None
    except Exception as e:
        log.error(e)
        return None
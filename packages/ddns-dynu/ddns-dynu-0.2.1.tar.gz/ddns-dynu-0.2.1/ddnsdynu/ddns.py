import requests
import json
import time
import sys
import daemon
from ddnsdynu import log
from ddnsdynu import ipaddr

ifname = None
api_base_url = "https://api.dynu.com/v2/"
api_key = ''

def make_api_headers(headers):
    if 'API-Key' not in headers:
        headers['API-Key'] = api_key
    if 'accept' not in headers:
        headers['accept'] = 'application/json'
    return headers

def get_dns_ids(hostname, record_type):
    url = api_base_url + "dns/record/" + hostname
    params = { "recordType": record_type }
    resp = requests.get(url, params=params, headers=make_api_headers({}))
    res = resp.json()
    log.info(res)
    if res['statusCode'] == 200:
        records = res['dnsRecords']
        if len(records) > 0:
            return records[0]['domainId'], records[0]['id'] 
    return None


def get_dns_record_ipv6(hostname, record_type):
    url = api_base_url + "dns/record/" + hostname
    params = { "recordType": record_type }
    resp = requests.get(url, params=params, headers=make_api_headers({}))
    res = resp.json()
    log.info(res)
    if res['statusCode'] == 200:
        records = res['dnsRecords']
        if len(records) > 0:
            return records[0]['ipv6Address']
    return None

def get_dns_record_ipv4(hostname, record_type):
    url = api_base_url + "dns/record/" + hostname
    params = { "recordType": record_type }
    resp = requests.get(url, params=params, headers=make_api_headers({}))
    res = resp.json()
    log.info(res)
    if res['statusCode'] == 200:
        records = res['dnsRecords']
        if len(records) > 0:
            return records[0]['ipv4Address']
    return None


def update_ipv6_record(hostname, ipv6):
    prev_ipv6 = get_dns_record_ipv6(hostname, 'AAAA')
    if prev_ipv6 == ipv6:
        return True
    
    domain_id, record_id = get_dns_ids(hostname, 'AAAA')
    log.info("%d %d" % (domain_id, record_id))
    url = api_base_url + "/dns/%d/record/%d" % (domain_id, record_id)
    payload = {
        "nodeName": hostname.split('.')[0],
        "recordType": "AAAA",
        "ttl": 30,
        "state": True,
        "group": "",
        "ipv6Address": ipv6
    }
    resp = requests.post(url, data=json.dumps(payload), headers=make_api_headers({}))
    res = resp.json()
    log.info(res)
    return res['statusCode'] == 200

def update_ipv4_record(hostname, ipv4):
    prev_ipv4 = get_dns_record_ipv4(hostname, 'A')
    if prev_ipv4 == ipv4:
        return True
    
    domain_id, record_id = get_dns_ids(hostname, 'A')
    log.info("%d %d" % (domain_id, record_id))
    url = api_base_url + "/dns/%d/record/%d" % (domain_id, record_id)
    payload = {
        "nodeName": hostname.split('.')[0],
        "recordType": "A",
        "ttl": 30,
        "state": True,
        "group": "",
        "ipv4Address": ipv4
    }
    resp = requests.post(url, data=json.dumps(payload), headers=make_api_headers({}))
    res = resp.json()
    log.info(res)
    return res['statusCode'] == 200

def update_ipv6_with_check(hostname, ifname):
    ipv6 = ipaddr.get_ipv6(ifname)
    log.info("check ipv6 %s" % ipv6)
    update_ipv6_record(hostname, ipv6)

def update_ipv4_with_check(hostname):
    ipv4 = ipaddr.get_ipv4_addr()
    log.info("check ipv4 %s" % ipv4)
    update_ipv4_record(hostname, ipv4)

def ddns(hostname, inet_type, ifname=None):
    if inet_type == '4':
        update_ipv4_with_check(hostname)
    elif inet_type == '6':
        update_ipv6_with_check(hostname, ifname)

def usage():
    print(
        "ddns-dynu d|t token hostname 4|6 [interface]\n"
        "[d|t]\n"
        "\td - daemon mode\n"
        "\tt - test mode (run onece directly)\n"
        "token\n"
        "\ttoken is file in daemon mode\n"
        "\ttoken is dynu.com token  in test mode\n"
        "[4|6]\n"
        "\t4 - ipv4\n"
        "\t6 - ipv6\n"
        "[interface]\n"
        "\tnetwork interface used for get ipv6 address"
    )
    exit()

def main():
    global api_key
    cmdargs = sys.argv[1:]
    if len(cmdargs) < 4:
        usage()
    run_type = cmdargs[0]
    key_arg = cmdargs[1]
    inet_type = cmdargs[3]
    ifname = ''
    if inet_type == '6':
        if len(cmdargs) < 5:
            usage()
        ifname = cmdargs[4]
    args = {
        'hostname': cmdargs[2],
        'inet_type': inet_type,
        'ifname': ifname
    }

    if run_type == 'd':
        with open(key_arg) as fp:
            api_key = fp.read().strip()
        with daemon.DaemonContext():
            log.init_log(True, log.LOG_DEBUG)
            log.info("ddns daemon starting")
            while True:
                try:
                    ddns(**args)
                except Exception as e:
                    log.error(e)
                time.sleep(30)
    elif run_type == 't':
        api_key = key_arg
        log.init_log(False, log.LOG_DEBUG)
        ddns(**args)

if __name__ == "__main__":
    main()

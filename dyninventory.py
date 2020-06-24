#!/usr/bin/env python
#  Simple script to pull devices from EM7/SL1 to Ansible WX/Tower
#
#  Scott Dozier Updated 5/4/2020
#
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from requests.auth import HTTPBasicAuth
import requests
import base64
import argparse
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
class Inventory():

    NAME = 'em7_inventory'
    
    def __init__(self, args,username= 'awxsvc', password=base64.b64decode("UzBuaXRDNTlwTFVybGhsc2VqcmI="), 
                uri='https://172.19.254.49/',verify_ssl=False):
                    
        self.inventory = {}
        self.args = args
        self.username = username
        self.password = password
        self.uri = uri
        self.verify = verify_ssl
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(username, password)
        
        
        if self.args.list:
            self.sysinfo = self._connect()
            self.inventory = self.dynamic_inventory()
        # If no groups or vars are present, return an empty inventory.
        else:
            self.inventory = self.empty_inventory()

        print(json.dumps(self.inventory))


    def _connect(self):
        info = self.get('api/sysinfo')
        return info.json()

    def get(self, uri, params=None):
        """
        Get a URI from the API

        :param uri: The URI
        :type  uri: ``str``

        :params params: Extra params
        :type   params: ``dict``
        """
        if params is None:
            params = {}
        if uri.startswith('/'):
            uri = uri[1:]
        return self.session.get('%s/%s' % (self.uri, uri),
                                params=params,
                                verify=self.verify,timeout=10)

    def devices(self, limit=80000):
        """
        Get a list of devices

        :param details: Get hostname/ip for physical devies
        :type  details: ``bool``
        
        :param limit: Number of devices to retrieve
        :type details: ``int``

        :rtype: ``list`` of :class:`Device`
        """
        
        #get list of organizations
        response = self.get('api/organization',  {'limit': limit})
        organizations = {}
        for org in response.json()['result_set']:
            organizations[ org['URI'].split('/')[-1]] = org['description']
        #get list of device hostnames
        response = self.get('api/device', {'link_disp_field': 'name', 'limit': limit,'filter.0.ip.contains': '.'})
        device_hostnames = {}
        for device in response.json()['result_set']:
            device_hostnames[ device['URI'].split('/')[-1]] = device['description']
        #get list of device ips
        response = self.get('api/device', {'link_disp_field': 'ip', 'limit': limit,'filter.0.ip.contains': '.'})
        device_ips = {}
        for device in response.json()['result_set']:
            device_ips[ device['URI'].split('/')[-1]] = device['description']
        #get list of device orgs
        response = self.get('api/device', {'link_disp_field': 'organization', 'limit': limit,'filter.0.ip.contains': '.'})
        device_org = {}
        for device in response.json()['result_set']:
            device_org[ device['URI'].split('/')[-1]] = device['description']
            
        devices = {}
        groups = []
        for device in device_ips.keys():
            additional_entries = ['qssmtp','qsops','alln1syspsp01','homd1is4','alln1qsutil01','alln1qsibsmtpp01','alln1qsyumrpp01','alln1sftpp01','alln1sftpp01']

            if 'v01' in device_hostnames[device] or 'v11' in device_hostnames[device] or 'v12' in device_hostnames[device] or '-vip' in device_hostnames[device].lower(): #ignore vips
                continue
            elif 'QS MoM_decom' in organizations[device_org[device]]: #ignore decom
                continue
            elif 'is4' in device_hostnames[device]:
                devices[device] = (device_hostnames[device],device_ips[device],[organizations[device_org[device]],'ALL','IS4'])  
            elif 'homd' in device_hostnames[device].lower() or 'hsbc' in device_hostnames[device].lower() or 'bofa' in device_hostnames[device].lower(): #ignore vdi customers
                continue              
            elif 'em7db' in device_hostnames[device] or 'em7he-db' in device_hostnames[device]:
                devices[device] = (device_hostnames[device],device_ips[device],[organizations[device_org[device]],'ALL','EM7','EM7DB'])
            elif 'em7prt' in device_hostnames[device] or 'em7he-ap' in device_hostnames[device]:
                devices[device] = (device_hostnames[device],device_ips[device],[organizations[device_org[device]],'ALL','EM7','EM7PRT'])
            elif 'em7mc' in device_hostnames[device] or 'em7he-mc' in device_hostnames[device]:
                devices[device] = (device_hostnames[device],device_ips[device],[organizations[device_org[device]],'ALL','EM7','EM7MC'])
            elif 'em7dc' in device_hostnames[device] or 'em7he-dc' in device_hostnames[device] or 'em7-dc' in device_hostnames[device]:
                devices[device] = (device_hostnames[device],device_ips[device],[organizations[device_org[device]],'ALL','EM7','EM7DC'])
            elif 'em7aio' in device_hostnames[device]:
                devices[device] = (device_hostnames[device],device_ips[device],[organizations[device_org[device]],'ALL','EM7','EM7AIO','EM7DB','EM7PRT','EM7DBVIP'])
            elif 'em7gm' in device_hostnames[device]:
                devices[device] = (device_hostnames[device],device_ips[device],[organizations[device_org[device]],'ALL','EM7','EM7GM'])
            elif 'spldpl' in device_hostnames[device]:
                devices[device] = (device_hostnames[device],device_ips[device],[organizations[device_org[device]],'ALL','SPL','SPLDPL'])  
            elif 'splaio' in device_hostnames[device]:
                devices[device] = (device_hostnames[device],device_ips[device],[organizations[device_org[device]],'ALL','SPL','SPLAIO'])  
            elif 'splind' in device_hostnames[device] or '-idx' in device_hostnames[device]:
                devices[device] = (device_hostnames[device],device_ips[device],[organizations[device_org[device]],'ALL','SPL','SPLIND'])  
            elif 'splma' in device_hostnames[device]:
                devices[device] = (device_hostnames[device],device_ips[device],[organizations[device_org[device]],'ALL','SPL','SPLMAS'])  
            elif 'splsrc' in device_hostnames[device]:
                devices[device] = (device_hostnames[device],device_ips[device],[organizations[device_org[device]],'ALL','SPL','SPLSRC'])  
            elif 'spl' in device_hostnames[device]:
                devices[device] = (device_hostnames[device],device_ips[device],[organizations[device_org[device]],'ALL','SPL'])  
            elif 'rly' in device_hostnames[device] or 'relay' in device_hostnames[device]:
                devices[device] = (device_hostnames[device],device_ips[device],[organizations[device_org[device]],'ALL','RLY'])    
  
            elif 'lnxjmp' in device_hostnames[device] or 'lnxauto' in device_hostnames[device]:
                #replace lnxauto with lnxjmp for customer lnxauto
                devices[device] = (device_hostnames[device].replace('lnxauto','lnxjmp'),device_ips[device],[organizations[device_org[device]],'ALL','LNXJMP'])    
            elif 'DB VIP' in device_hostnames[device] : 
                devices[device] = (device_hostnames[device].replace(' ','_'),device_ips[device],[organizations[device_org[device]],'ALL','EM7DBVIP'])    
            elif any(prefix in device_hostnames[device] for prefix in additional_entries):
                devices[device] = (device_hostnames[device],device_ips[device],[organizations[device_org[device]],'ALL'])    
                                                                         
                                                                                        
        return devices
        

        
    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}
        
    def dynamic_inventory(self):
        devices = self.devices()
        inventory = {}
        #get groups
        for device in devices:
            for group in devices[device][2]:
                group = group.replace(' ','_').replace('&','_').replace('-','_')
                if group in inventory:
                    inventory[group]['hosts'].append(devices[device][0])
                else:
                    inventory[group] = {}
                    inventory[group]['hosts']=[devices[device][0]]
        
        #get host meta
        hostvars = {}
        for device in devices:
             hostvars[devices[device][0]]= {}
             hostvars[devices[device][0]]["ansible_host"] = devices[device][1]
        inventory['_meta'] = {'hostvars': hostvars}
        return inventory
        
# Main function
def main():
    # Read command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', action = 'store_true')
    args = parser.parse_args()
    # Get the inventory.
    Inventory(args)


if __name__ == '__main__':
    main()



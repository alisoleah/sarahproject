#!/usr/bin/python

import requests
import json
import urllib3
from ansible.module_utils.basic import AnsibleModule

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class VPLEXClient:
    def __init__(self, vplexhost, vplexuser, vplexpassword):
        self.vplexhost = vplexhost
        self.vplexuser = vplexuser
        self.vplexpassword = vplexpassword
        self.base_url = f"https://{vplexhost}/vplex/v2"
        self.session = requests.Session()
        self.session.auth = (vplexuser, vplexpassword)
        self.session.verify = False  
        
    def get_directors(self):
        url = f"{self.base_url}/directors"
        response = self.session.get(url)
        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to get directors: {response.status_code} {response.text}")
            return None
        directors = response.json()
        director_names = [director['name'] for director in directors]
        return director_names
    
    def get_director_ports_pwwns(self, director_name):
        url = f"{self.base_url}/directors/{director_name}/ports"
        response = self.session.get(url)
        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to get ports for {director_name}: {response.status_code} {response.text}")
            return None
        ports = response.json()
        pwwns = [self.convert_pwwn(port['address']) for port in ports if (port['address'] != "0x0000000000000000" and port['address'].startswith("0x")) and len(port['address']) == 18 ]
        return pwwns

    def get_director_port(self, director_name, pwwn):
        url = f"{self.base_url}/directors/{director_name}/ports?address={pwwn}"
        response = self.session.get(url)
        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to get port info for {director_name}: {response.status_code} {response.text}")
            return None
        port = response.json()
        return port
        
    def get_all_pwwns(self):
        all_pwwns = []
        director_names = self.get_directors()
        for director_name in director_names:
            pwwns = self.get_director_ports_pwwns(director_name)
            all_pwwns.extend(pwwns)
        return all_pwwns   
    
    def convert_pwwn(self, pwwn):
        # Remove the '0x' prefix if present
        if pwwn.startswith('0x'):
            pwwn = pwwn[2:]        
        # Split the PWWN into pairs of characters
        pairs = [pwwn[i:i+2] for i in range(0, len(pwwn), 2)]        
        # Join the pairs with colons
        normal_format = ':'.join(pairs)       
        return normal_format  
    
    def convert_pwwn_to_decimal(self, pwwn):
        # Remove colons from the pWWN
        decimal_format = pwwn.replace(':', '')
        # Add the prefix
        decimal_format = '0x' + decimal_format
        return decimal_format
    
    def get_pwwn_info(self, pwwn):
        pwwn = self.convert_pwwn_to_decimal(pwwn)
        director_names = self.get_directors()
        for director_name in director_names:
            pwwn_info = self.get_director_port(director_name, pwwn)
            if len(pwwn_info) > 0:
                return pwwn_info[0]['name']
        return None          

def run_module():
    module_args = dict(
        vplexhost=dict(type='str', required=True),
        vplexuser=dict(type='str', required=True),
        vplexpassword=dict(type='str', required=True, no_log=True)
    )

    result = dict(
        changed=False,
        wwpn_list=[]
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    vplexhost = module.params['vplexhost']
    vplexuser = module.params['vplexuser']
    vplexpassword = module.params['vplexpassword']

    try:
        client = VPLEXClient(vplexhost, vplexuser, vplexpassword)
        result['wwpn_list'] = client.get_all_pwwns()
    except Exception as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


def main():
    run_module()

if __name__ == '__main__':
    main()


#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from storops import UnitySystem
import urllib3
import json

def remove_first_8_octets(wwpn):
    return ':'.join(wwpn.split(':')[8:])

def run_module():
    # Define the module's arguments
    module_args = dict(
        unispherehost=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True)
    )

    # Create the Ansible module
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Extract the parameters
    unispherehost = module.params['unispherehost']
    username = module.params['username']
    password = module.params['password']

    # Suppress warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Connect to the Unity system
    try:
        unity = UnitySystem(unispherehost, username, password)
        fc_ports = unity.get_fc_port()
        result = [json.loads(str(port))['UnityFcPort']['wwn'] for port in fc_ports]
        wwpn_list = [remove_first_8_octets(wwpn) for wwpn in result]


        # Return the result
        module.exit_json(changed=False, wwpn_list=wwpn_list)
    except Exception as e:
        module.fail_json(msg=str(e))

def main():
    run_module()

if __name__ == '__main__':
    main()
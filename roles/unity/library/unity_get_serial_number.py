#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from storops import UnitySystem
import urllib3
import json

def run_module():
    # Define the module's arguments
    module_args = dict(
        unispherehost=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
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
        serial_number = unity.serial_number



        # Return the result
        module.exit_json(changed=False, serial_number=serial_number)
    except Exception as e:
        module.fail_json(msg=str(e))

def main():
    run_module()

if __name__ == '__main__':
    main()

#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from storops import UnitySystem
import json

def run_module():
    module_args = dict(
        unispherehost=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        pwwn=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        port_name=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    unispherehost = module.params['unispherehost']
    username = module.params['username']
    password = module.params['password']
    pwwn = module.params['pwwn']

    try:
        unity = UnitySystem(unispherehost, username, password)
        fc_ports = unity.get_fc_port()
        for port in fc_ports:
            current_port = json.loads(str(port))['UnityFcPort']['wwn']
            if current_port.endswith(pwwn):
                result['port_name'] = json.loads(str(port))['UnityFcPort']['id']
                module.exit_json(**result)
        module.fail_json(msg="No matching FC port found for the given pwwn.")
    except Exception as e:
        module.fail_json(msg=str(e))

def main():
    run_module()

if __name__ == '__main__':
    main()
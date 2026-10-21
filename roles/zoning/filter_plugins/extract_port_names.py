from ansible.errors import AnsibleFilterError
def extract_port_names(cmd_output):
    try:
        lines = cmd_output
        port_names = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 3: 
                port_name = parts[2]  # Assuming the PORT NAME is the third column
                port_names.append(port_name[1:])
        return port_names
    except Exception as e:
        raise AnsibleFilterError('Error extracting port names: %s' % str(e))

class FilterModule(object):
    def filters(self):
        return {
            'extract_port_names': extract_port_names
        }

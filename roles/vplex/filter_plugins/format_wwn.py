from ansible.errors import AnsibleFilterError

def format_wwn(unformatted_wwn):
    if not isinstance(unformatted_wwn, str):
        raise AnsibleFilterError("Input must be a string")
    return unformatted_wwn.replace(":", "").lower()

class FilterModule(object):
    def filters(self):
        return {
            'format_wwn': format_wwn
        }


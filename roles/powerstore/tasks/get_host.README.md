# get_host.yml - Explanation

## Purpose
This task checks if a specific host already exists on the PowerStore storage array.

## Input Variables
- `node_hostname` - The hostname of the server to search for (provided by user in vars file)
- `array_hostname` - The name of the PowerStore array (provided by user in vars file)
- Connection credentials (from `storage_array_vars.yml`):
  - `{array_hostname}_array_ip`
  - `{array_hostname}_user`
  - `{array_hostname}_password`
  - `{array_hostname}_validate_certs`

## Output Variables
- `found_host_flag` - Boolean: `true` if host exists, `false` if not
- `found_host` - The actual host name if found (empty if not found)

## Step-by-Step Explanation

### Step 1: Query PowerStore for ALL hosts
```yaml
- name: Get Hosts Details
  dellemc.powerstore.info:
    array_ip: "{{ lookup('vars', array_hostname + '_array_ip') }}"
    user: "{{ lookup('vars', array_hostname + '_user') }}"
    password: "{{ lookup('vars', array_hostname + '_password') }}"
    validate_certs: "{{ lookup('vars', array_hostname + '_validate_certs') }}"
    gather_subset:
      - host
    all_pages: true
  register: host_results
```

**What this does:**
- Connects to PowerStore using credentials from `storage_array_vars.yml`
- Asks PowerStore: "Give me a list of ALL hosts registered on this array"
- `all_pages: true` ensures we get all hosts (not just first 100)
- Stores the result in `host_results` variable

**Example output:**
```
host_results.Hosts:  # Note: Capital H
  - name: "webserver01"
    id: "abc-123"
  - name: "dbserver01"
    id: "def-456"
  - name: "appserver01"
    id: "ghi-789"
```

**Important:** PowerStore uses `Hosts` (capital H), not `hosts` (lowercase). This was verified through testing.

### Step 2: Extract just the host names
```yaml
- name: Obtain the names of the hosts
  ansible.builtin.set_fact:
    host_names: "{{ host_results.Hosts | map(attribute='name') | list }}"
```

**What this does:**
- Takes the full host objects and extracts only the `name` attribute
- Creates a simple list: `["webserver01", "dbserver01", "appserver01"]`

**Jinja2 filter explanation:**
- `map(attribute='name')` - Extract the 'name' field from each object
- `list` - Convert the result to a list

### Step 3: Search for our specific host
```yaml
- name: Look for the host in the hosts found
  ansible.builtin.set_fact:
    found_host: "{{ host_names | select('search', node_hostname) | list }}"
```

**What this does:**
- If `node_hostname` = "webserver01" (from user's vars file)
- It searches the list for anything containing "webserver01"
- Result: `["webserver01"]` (if found) or `[]` (if not found)

**Jinja2 filter explanation:**
- `select('search', node_hostname)` - Filter list for items containing `node_hostname`
- `list` - Convert result to a list

**Example:**
```
host_names = ["webserver01", "dbserver01", "appserver01"]
node_hostname = "webserver01"
Result: ["webserver01"]
```

### Step 4: Set a flag (true/false)
```yaml
- name: Set found_host_flag
  ansible.builtin.set_fact:
    found_host_flag: "{{ found_host | length > 0 }}"
```

**What this does:**
- If list has items (length > 0) → `found_host_flag = true`
- If list is empty (length = 0) → `found_host_flag = false`

**Example:**
```
found_host = ["webserver01"]
found_host | length = 1
found_host_flag = true
```

### Step 5: Get the actual host name if found
```yaml
- name: Set foundhost
  ansible.builtin.set_fact:
    found_host: "{{ found_host[0] }}"
  when: found_host_flag
```

**What this does:**
- If host was found, extract the first (and only) item from the list
- Sets `found_host = "webserver01"`
- Only runs when `found_host_flag = true`

### Step 6: Print the result
```yaml
- name: Print the name of the found host
  ansible.builtin.debug:
    msg: "Found: {{ found_host_flag }} Host: {{ found_host }}"
```

**What this does:**
- Displays the result to the user
- Example output: `Found: true Host: webserver01`

## Usage in Workflow

Later in the workflow, we use these variables:

```yaml
- name: Create host in the array
  when: not found_host_flag  # Only create if NOT found
  ansible.builtin.include_role:
    name: powerstore
    tasks_from: create_host_with_initiators.yml
```

This prevents:
- Creating duplicate hosts
- Errors from trying to create a host that already exists

## Testing Notes

**✅ VERIFIED:** The exact structure of `host_results` from PowerStore has been verified through testing.
- PowerStore uses: `host_results.Hosts` (capital H) - CONFIRMED
- The structure includes: `id` and `name` for each host
- Example actual output from PowerStore 4.4.0.0:
  ```yaml
  host_results.Hosts:
    - id: "20b6c52d-a4c7-4b2f-81c9-507688553ce6"
      name: "SUNT5120-B"
    - id: "236b2c9f-9bc4-4082-b26a-d0d1d05334e9"
      name: "csi-node-d58f8ceeb57a42cf83d898e2369cebb9-10.241.167.88"
  ```

**Test Results:**
- Connection to PowerStore: ✅ Successful
- Host retrieval: ✅ Successful (retrieved 34 hosts)
- Host name extraction: ✅ Successful
- Host search: ✅ Working correctly
- Flag setting: ✅ Working correctly

**Test command:**
```bash
ansible-playbook powerstore_test_get_host.yml
```

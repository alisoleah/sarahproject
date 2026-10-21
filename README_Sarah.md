# Curia Phase 1 - Storage Automation Project

## Overview

This project provides Ansible playbooks and roles for automating Fibre Channel (FC) storage provisioning across multiple storage platforms including Dell EMC Unity, VPLEX, and Cisco Nexus switches. The automation handles zoning configuration, host registration, volume creation, and volume mapping for ESXi, Linux, and Windows hosts.

## Project Structure

```
curia_phase1/
├── playbooks/
│   ├── files/          # Standalone playbook files
│   ├── tasks/          # Reusable task files
│   ├── templates/      # Jinja2 templates
│   └── vars/           # Variable files
└── roles/
    ├── common/         # Common tasks shared across roles
    ├── unity/          # Dell EMC Unity storage array tasks
    ├── vmware/         # VMware vCenter/ESXi tasks
    ├── vplex/          # Dell EMC VPLEX virtualization tasks
    └── zoning/         # Cisco Nexus FC zoning tasks
```

## Roles Overview

### 1. Common Role (`roles/common/`)
Shared utility tasks used across multiple roles.

**Tasks:**
- `get_node_details.yml` - Prompts user for node IP, username, and password (for Linux/Windows nodes)

### 2. Zoning Role (`roles/zoning/`)
Handles Fibre Channel zoning configuration on Cisco Nexus switches.

**Main Workflow:** `workflow.yml`

**Tasks:**
- `get_storage_array_aliases.yml` - Retrieves storage array device aliases from switch
- `get_node_aliases.yml` - Retrieves node device aliases from switch
- `get_esxi_node_pwwns.yml` - Gets FC PWWNs from ESXi host via vCenter
- `get_lin_node_pwwns.yml` - Gets FC PWWNs from Linux host via SSH
- `get_win_node_pwwns.yml` - Gets FC PWWNs from Windows host via WinRM
- `get_fcns_found_pwwns.yml` - Queries FCNS database to find PWWNs logged into switch
- `create_device_aliases.yml` - Creates device aliases on switch for node ports
- `recheck_node_aliases.yml` - Verifies device aliases were created successfully
- `create_zones.yml` - Creates FC zones between node and storage array aliases

### 3. Unity Role (`roles/unity/`)
Manages Dell EMC Unity storage array operations.

**Tasks:**
- `create_volume.yml` - Creates a block storage volume on Unity
- `create_host_with_initiators.yml` - Creates a host entry with FC initiators on Unity
- `find_initiator.yml` - Checks if an initiator exists on the Unity array
- `get_host.yml` - Retrieves host information from Unity
- `get_host_initiators.yml` - Gets FC initiators for a host from Unity
- `get_serial_number.yml` - Gets Unity array serial number
- `get_storage_pools.yml` - Lists available storage pools on Unity
- `get_volume_mapped_hosts.yml` - Gets list of hosts mapped to a volume
- `map_volume.yml` - Maps a volume to a single host
- `map_volume_multiple_hosts.yml` - Maps a volume to multiple hosts
- `modify_volume.yml` - Modifies volume properties (size, thin provisioning, etc.)
- `unmap_volume_multiple_hosts.yml` - Unmaps volume from multiple hosts

### 4. VMware Role (`roles/vmware/`)
Handles VMware vCenter and ESXi operations.

**Tasks:**
- `get_cluster_hosts.yml` - Retrieves list of ESXi hosts in a vCenter cluster
- `format_hosts_to_dict.yml` - Formats host list into dictionary structure

### 5. VPLEX Role (`roles/vplex/`)
Manages Dell EMC VPLEX storage virtualization operations.

**Tasks:**
- `add_volume_to_cg.yml` - Adds volume to consistency group
- `add_volume_to_storage_view.yml` - Adds volume to storage view
- `claim_storage_volume.yml` - Claims storage volume in VPLEX
- `create_distributed_device.yml` - Creates distributed device across VPLEX clusters
- `create_distributed_volume.yml` - Creates distributed virtual volume
- `create_extent.yml` - Creates extent from storage volume
- `create_host_initiators.yml` - Creates host initiator entries in VPLEX
- `create_local_device.yml` - Creates local device in VPLEX
- `create_storage_view.yml` - Creates storage view for host access
- `create_virtual_volume.yml` - Creates local virtual volume
- `find_initiator.yml` - Checks if initiator exists in VPLEX
- `get_detach_rule.yml` - Retrieves detach rule information
- `get_distributed_volume.yml` - Gets distributed volume details
- `get_storage_view.yml` - Gets storage view details
- `get_storage_volume.yml` - Gets storage volume details
- `get_vplex_cluster.yml` - Gets VPLEX cluster information
- `get_vplex_unity_host.yml` - Gets VPLEX host name in Unity
- `rediscover_array.yml` - Rediscover storage array in VPLEX
- `rediscover_initiators.yml` - Rediscover initiators in VPLEX
- `remove_volume_from_storage_view.yml` - Removes volume from storage view
- `set_array_1_vars.yml` - Sets variables for array 1 configuration
- `set_array_2_vars.yml` - Sets variables for array 2 configuration
- `set_distributed_volume_parameters.yml` - Sets distributed volume parameters
- `set_virtual_pool_vars.yml` - Sets virtual pool configuration
- `set_volume_parameters.yml` - Sets volume parameters

## Playbook Files

### SAN Zoning Playbooks

**`san_create_zones.yml`** - Creates FC zones between node and storage array
- Runs on: `switch1, switch2`
- Dependencies: zoning role tasks
- Workflow:
  1. Get storage array aliases from switch
  2. Get node aliases from switch
  3. If node aliases not found:
     - Get node PWWNs (ESXi/Linux/Windows)
     - Create device aliases
     - Verify aliases created
  4. Create zones between node and array aliases

**`san_create_array_device_aliases.yml`** - Creates device aliases for storage array ports
**`san_delete_host_zones.yml`** - Deletes zones for a specific host
**`san_host_zones_information.yml`** - Retrieves zone information for a host

### Unity Playbooks

**`unity_create_volume.yml`** - Creates a volume on Unity array
**`unity_delete_volume.yml`** - Deletes a volume from Unity array
**`unity_list_storage_pools.yml`** - Lists available storage pools
**`unity_map_volume_to_hosts.yml`** - Maps volume to multiple hosts
**`unity_map_volume_to_single_host.yml`** - Maps volume to single host with full workflow
- Runs on: `switch1, switch2`
- Dependencies: zoning, unity roles
- Workflow:
  1. Run zoning workflow (create aliases and zones)
  2. Find host on Unity array
  3. If host not found, get initiators and create host
  4. Map volume to host
**`unity_modify_volume.yml`** - Modifies volume properties
**`unity_unmap_volume.yml`** - Unmaps volume from single host
**`unity_unmap_volume_from_hosts.yml`** - Unmaps volume from multiple hosts

### VPLEX Playbooks

**`vplex_create_volume.yml`** - Creates volume in VPLEX with full workflow
- Play 1: Runs on localhost
  - Creates volumes on Unity arrays (1 or 2 arrays for metro)
  - Creates devices in VPLEX
  - Creates local or distributed virtual volumes
- Play 2: Runs on switches
  - Creates storage views
  - Maps hosts to volumes
  - Configures zoning

**`vplex_create_volume_enhanced.yml`** - Enhanced VPLEX volume creation with additional features
**`vplex_map_hosts_to_volume.yml`** - Maps hosts to existing VPLEX volume
**`vplex_unmap_hosts_from_volume.yml`** - Unmaps hosts from VPLEX volume

## Task Dependencies and Workflows

### Zoning Workflow (`roles/zoning/tasks/workflow.yml`)

```
get_storage_array_aliases.yml
    ↓
get_node_aliases.yml
    ↓
    ├─→ If aliases NOT found:
    │   ├─→ get_esxi_node_pwwns.yml (if ESXi)
    │   ├─→ get_node_details.yml (if Linux/Windows)
    │   ├─→ get_lin_node_pwwns.yml (if Linux)
    │   ├─→ get_win_node_pwwns.yml (if Windows)
    │   ├─→ get_fcns_found_pwwns.yml
    │   ├─→ create_device_aliases.yml
    │   └─→ recheck_node_aliases.yml
    │
    └─→ create_zones.yml (always runs)
```

**Dependencies:**
- `get_storage_array_aliases.yml` requires: `array_hostname` variable
- `get_node_aliases.yml` requires: `node_hostname` variable
- `get_esxi_node_pwwns.yml` requires: `node_hostname`, `domain`, `vcenter` credentials
- `get_lin_node_pwwns.yml` requires: `node_ip`, `node_user`, `node_password` (from `get_node_details.yml`)
- `get_win_node_pwwns.yml` requires: `node_ip`, `node_user`, `node_password` (from `get_node_details.yml`)
- `get_fcns_found_pwwns.yml` requires: `node_pwwn_list` (from PWWN tasks)
- `create_device_aliases.yml` requires: `switch_node_pwwn_list`, `node_type`, `node_hostname`
- `recheck_node_aliases.yml` requires: `node_hostname`
- `create_zones.yml` requires: `node_aliases_list`, `array_aliases_list`

### Unity Host Creation Workflow (`roles/unity/tasks/create_host_with_initiators.yml`)

```
Pause (60 seconds)
    ↓
Get FC initiators from Unity
    ↓
Initialize found_initiator_list
    ↓
find_initiator.yml (loop through combined_initiators_list)
    ↓
Map node_type to Unity OS type
    ↓
Create Host with Initiators
    ↓
Set found_host variable
```

**Dependencies:**
- Requires: `array_hostname`, Unity credentials (via lookup)
- Requires: `combined_initiators_list` (list of node PWWNs)
- Requires: `node_hostname`, `node_type`
- Calls: `find_initiator.yml` (subtask)
- Produces: `found_host`, `found_initiator_list`

### VPLEX Volume Creation Workflow (`playbooks/files/vplex_create_volume.yml`)

**Play 1 - Array Operations (localhost):**

```
For Array 1 (and Array 2 if metro):
    ├─→ Set array_hostname, pool_name, vol_name
    ├─→ create_volume.yml (Unity)
    ├─→ get_vplex_unity_host.yml
    ├─→ map_volume.yml (Unity)
    ├─→ get_vplex_cluster.yml
    ├─→ get_serial_number.yml (Unity)
    ├─→ rediscover_array.yml
    ├─→ get_storage_volume.yml
    ├─→ claim_storage_volume.yml
    ├─→ create_extent.yml
    ├─→ create_local_device.yml
    ├─→ set_array_1_vars.yml / set_array_2_vars.yml
    ├─→ create_virtual_volume.yml (if not metro)
    └─→ create_distributed_device.yml + create_distributed_volume.yml (if metro)
```

**Play 2 - Mapping and Zoning (switches):**

```
set_virtual_pool_vars.yml
    ↓
If vCenter cluster:
    ├─→ get_cluster_hosts.yml
    └─→ format_hosts_to_dict.yml
    ↓
Set facts for clusters and volumes
    ↓
vplex_create_storage_view.yml (loop through hosts)
```

**Dependencies:**
- Unity tasks require: Unity array credentials, pool names, volume parameters
- VPLEX tasks require: VPLEX credentials, cluster names
- Mapping requires: Host information (from VMware or manual input)
- Storage view creation requires: VPLEX ports, initiator lists

### Unity Map Volume to Single Host Workflow (`playbooks/files/unity_map_volume_to_single_host.yml`)

```
zoning/workflow.yml
    ↓
get_host.yml (Unity)
    ↓
If host not found:
    ├─→ get_host_initiators.yml
    └─→ create_host_with_initiators.yml
    ↓
map_volume.yml
```

**Dependencies:**
- Requires zoning to complete first (zones must exist)
- Requires Unity host to exist or be created
- Requires volume to exist on Unity

## Key Variables

### Common Variables
- `node_hostname` - Hostname of the server
- `node_type` - Type of node: `esxi`, `linux`, `windows`
- `array_hostname` - Name of the storage array
- `validate_certs` - SSL certificate validation flag

### Zoning Variables
- `node_aliases_found_flag` - Boolean: node aliases exist on switch
- `array_aliases_found_flag` - Boolean: array aliases exist on switch
- `node_aliases_list` - List of node device aliases
- `array_aliases_list` - List of array device aliases
- `node_pwwn_list` - List of node FC PWWNs
- `switch_node_pwwn_list` - PWWNs found on switch
- `zone_vsan` - VSAN ID for zoning
- `zoneset_name` - Name of the zoneset

### Unity Variables
- `vol_name` - Volume name
- `pool_name` - Storage pool name
- `size_gb` - Volume size in GB
- `is_thin` - Thin provisioning flag
- `compression` - Compression flag
- `advanced_dedup` - Advanced deduplication flag
- `found_host` - Host found on Unity
- `found_initiator_list` - List of initiators found on Unity

### VPLEX Variables
- `vplex_array` - VPLEX array identifier
- `is_metro` - Metro cluster configuration flag
- `distributed_device` - Distributed device name
- `distributed_virtual_volume` - Distributed volume name
- `virtual_volume` - Local virtual volume name
- `array_1_cluster` - Cluster name for array 1
- `array_2_cluster` - Cluster name for array 2
- `vplex_initiators_list` - List of VPLEX initiators

### VMware Variables
- `vcenter` - vCenter server identifier
- `is_vcenter_cluster` - Boolean: target is vCenter cluster
- `domain` - Domain name for ESXi hosts

## Usage Examples

### Create Zones for a Host
```bash
ansible-playbook -i playbooks/files/inventory.ini playbooks/files/san_create_zones.yml
```

### Create and Map Volume to Single Host
```bash
ansible-playbook -i playbooks/files/inventory.ini playbooks/files/unity_map_volume_to_single_host.yml
```

### Create VPLEX Volume
```bash
ansible-playbook -i playbooks/files/inventory.ini playbooks/files/vplex_create_volume.yml
```

## Prerequisites

- Ansible 2.9 or higher
- Python 3.6 or higher
- Required Ansible collections:
  - `cisco.nxos` - For Cisco Nexus switch configuration
  - `dellemc.unity` - For Unity array management
  - `dellemc.vplex` - For VPLEX management
  - `community.vmware` - For VMware/vCenter operations
  - `ansible.windows` - For Windows host operations

## Notes

- The project uses device aliases to simplify FC zoning management
- Automatic alias naming convention: `auto_<hostname>_fc_<number>` for Linux/Windows, `auto_<hostname>_<vmhba>` for ESXi
- Zone naming convention: `auto_<node_alias>_<array_alias>`
- Storage view naming convention: `sv_<hostname>_<cluster>`
- All tasks include error handling with rescue blocks
- The workflow supports both local and metro VPLEX configurations

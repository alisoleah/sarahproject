# Curia Storage Automation - Repository Map

## Repository Structure

```
curia-storage-automation/
├── .git/
├── .gitignore
├── curia_phase1.tar.gz (ignored)
├── README_Sarah.md
├── POWERSTORE_IMPLEMENTATION_TRACKER.txt
├── playbooks/
│   ├── files/           # Standalone playbook files
│   ├── tasks/           # Reusable task files
│   ├── templates/       # Jinja2 templates
│   └── vars/            # Variable files
└── roles/
    ├── common/          # Shared utility tasks
    ├── unity/           # Dell EMC Unity storage
    ├── vmware/          # VMware vCenter/ESXi
    ├── vplex/           # Dell EMC VPLEX virtualization
    ├── powerstore/      # Dell EMC PowerStore
    └── zoning/          # Cisco Nexus FC zoning
```

## Directory Details

### Playbooks/files/ (Standalone Playbooks)
```
playbooks/files/
├── ansible.cfg                    # Ansible configuration
├── inventory.ini                  # Inventory file
├── inventory.ini.bkp              # Backup inventory
├── debug_vars.yml                 # Debug playbook
├── simple_test.yml                # Simple test playbook
├── test.yml                       # Test playbook
│
├── SAN Zoning Playbooks:
│   ├── san_create_zones.yml
│   ├── san_create_array_device_aliases.yml
│   ├── san_delete_host_zones.yml
│   └── san_host_zones_information.yml
│
├── Unity Storage Playbooks:
│   ├── unity_create_volume.yml
│   ├── unity_delete_volume.yml
│   ├── unity_list_storage_pools.yml
│   ├── unity_map_volume_to_hosts.yml
│   ├── unity_map_volume_to_single_host.yml
│   ├── unity_modify_volume.yml
│   ├── unity_unmap_volume.yml
│   └── unity_unmap_volume_from_hosts.yml
│
├── VPLEX Playbooks:
│   ├── vplex_create_volume.yml
│   ├── vplex_create_volume_enhanced.yml
│   ├── vplex_map_hosts_to_volume.yml
│   └── vplex_unmap_hosts_from_volume.yml
│
└── PowerStore Playbooks:
    ├── powerstore_create_hosts.yml        # Create multiple hosts with zoning
    ├── powerstore_create_host.yml         # Create single host with zoning (NEW)
    ├── powerstore_map_volume_to_host.yml  # Map volume to existing host (NEW)
    ├── powerstore_test_get_host.yml
    └── powerstore_test_host_only.yml
```

### Playbooks/tasks/ (Reusable Task Files)
```
playbooks/tasks/
├── powerstore_host_prepare.yml
├── unity_map_volume_prepare.yml
├── vplex_create_storage_view.yml
└── vplex_unmap_storage_view.yml
```

### Playbooks/vars/ (Variable Files)
```
playbooks/vars/
├── storage_array_vars.yml
├── vcenter_vars.yml
├── unity_test_vars.yml
├── zoning_delete_host_zones_vars.yml
├── san_*.yml (zoning variables)
├── unity_*.yml (Unity variables)
├── vplex_*.yml (VPLEX variables)
├── powerstore_test_create_host_vars.yml
├── powerstore_test_get_host_vars.yml
├── powerstore_create_host_vars.yml          # Variables for single host creation (NEW)
└── powerstore_map_volume_to_host_vars.yml   # Variables for volume mapping (NEW)
```

### Roles/ (Ansible Roles)

#### roles/common/
```
roles/common/
├── README.md
├── defaults/main.yml
├── handlers/main.yml
├── meta/main.yml
├── tasks/
│   └── get_node_details.yml
├── tests/
│   ├── inventory
│   └── test.yml
└── vars/main.yml
```

#### roles/zoning/
```
roles/zoning/
├── README.md
├── defaults/main.yml
├── handlers/main.yml
├── meta/main.yml
├── tasks/
│   ├── workflow.yml                    # Main zoning workflow
│   ├── get_storage_array_aliases.yml
│   ├── get_node_aliases.yml
│   ├── get_esxi_node_pwwns.yml
│   ├── get_lin_node_pwwns.yml
│   ├── get_win_node_pwwns.yml
│   ├── get_fcns_found_pwwns.yml
│   ├── create_device_aliases.yml
│   ├── recheck_node_aliases.yml
│   ├── create_zones.yml
│   ├── create_array_device_aliases.yml
│   ├── get_alias_zones.yml
│   ├── get_host_initiators.yml
│   ├── get_storage_array_port_info.yml
│   ├── get_storage_array_ports_info.yml
│   └── get_storage_array_pwwns.yml
├── filter_plugins/
│   ├── decimal_to_formatted_hex.py
│   └── extract_port_names.py
├── library/
│   ├── unity_fc_ports.py
│   ├── unity_port_info.py
│   ├── vplex_fc_ports.py
│   └── vplex_port_info.py
├── tests/
│   ├── inventory
│   └── test.yml
└── vars/main.yml
```

#### roles/unity/
```
roles/unity/
├── README.md
├── defaults/main.yml
├── handlers/main.yml
├── meta/main.yml
├── tasks/
│   ├── create_volume.yml
│   ├── create_host_with_initiators.yml
│   ├── delete_volume.yml
│   ├── find_initiator.yml
│   ├── get_host.yml
│   ├── get_host_initiators.yml.bkp
│   ├── get_serial_number.yml
│   ├── get_storage_pools.yml
│   ├── get_volume_mapped_hosts.yml
│   ├── map_volume.yml
│   ├── map_volume_multiple_hosts.yml
│   ├── modify_volume.yml
│   └── unmap_volume_multiple_hosts.yml
├── library/
│   ├── unity_get_serial_number.py
│   └── unity_volume_hosts.py
├── tests/
│   ├── inventory
│   └── test.yml
└── vars/main.yml
```

#### roles/vplex/
```
roles/vplex/
├── README.md
├── defaults/main.yml
├── handlers/main.yml
├── meta/main.yml
├── tasks/
│   ├── main.yml
│   ├── add_volume_to_cg.yml
│   ├── add_volume_to_storage_view.yml
│   ├── claim_storage_volume.yml
│   ├── create_distributed_device.yml
│   ├── create_distributed_volume.yml
│   ├── create_extent.yml
│   ├── create_host_initiators.yml
│   ├── create_local_device.yml
│   ├── create_storage_view.yml
│   ├── create_virtual_volume.yml
│   ├── find_initiator.yml
│   ├── get_detach_rule.yml
│   ├── get_distributed_volume.yml
│   ├── get_storage_view.yml
│   ├── get_storage_volume.yml
│   ├── get_vplex_cluster.yml
│   ├── get_vplex_unity_host.yml
│   ├── rediscover_array.yml
│   ├── rediscover_initiators.yml
│   ├── remove_volume_from_storage_view.yml
│   ├── set_array_1_vars.yml
│   ├── set_array_2_vars.yml
│   ├── set_distributed_volume_parameters.yml
│   ├── set_virtual_pool_vars.yml
│   └── set_volume_parameters.yml
├── filter_plugins/
│   └── format_wwn.py
├── tests/
│   ├── inventory
│   └── test.yml
└── vars/main.yml
```

#### roles/vmware/
```
roles/vmware/
├── README.md
├── defaults/main.yml
├── handlers/main.yml
├── meta/main.yml
├── tasks/
│   ├── main.yml
│   ├── get_cluster_hosts.yml
│   └── format_hosts_to_dict.yml
├── tests/
│   ├── inventory
│   └── test.yml
└── vars/main.yml
```

#### roles/powerstore/
```
roles/powerstore/
├── README.md
├── defaults/main.yml
├── handlers/main.yml
├── meta/main.yml
├── tasks/
│   ├── main.yml
│   ├── create_host_with_initiators.yml
│   ├── find_initiator.yml
│   ├── get_host.yml
│   ├── get_host.README.md
│   └── map_volume.yml                  # NEW: Volume mapping task
├── tests/
│   ├── inventory
│   └── test.yml
└── vars/main.yml
```

## Workflow Diagrams

### 1. Zoning Workflow (roles/zoning/tasks/workflow.yml)

```
┌─────────────────────────────────────────────────────────────┐
│                    ZONING WORKFLOW                            │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│ get_storage_array_   │
│ aliases.yml          │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ get_node_aliases.yml │
└──────────┬───────────┘
           │
           ▼
    ┌──────────────┐
    │ Aliases      │
    │ Found?       │
    └──────┬───────┘
           │
     NO ───┴─── YES
     │            │
     ▼            │
┌──────────────────────────────┐
│ Get Node PWWNs:             │
│ - get_esxi_node_pwwns.yml   │
│ - get_lin_node_pwwns.yml    │
│ - get_win_node_pwwns.yml    │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────┐
│ get_fcns_found_      │
│ pwwns.yml            │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ create_device_      │
│ aliases.yml          │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ recheck_node_        │
│ aliases.yml          │
└──────────┬───────────┘
           │
           └──────────┐
                      │
                      ▼
           ┌──────────────────────┐
           │ create_zones.yml     │
           └──────────────────────┘
```

### 2. Unity Map Volume to Single Host Workflow

```
┌─────────────────────────────────────────────────────────────┐
│         UNITY MAP VOLUME TO SINGLE HOST                      │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│ Zoning Workflow      │
│ (roles/zoning)       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ get_host.yml         │
│ (Unity)              │
└──────────┬───────────┘
           │
           ▼
    ┌──────────────┐
    │ Host Found?  │
    └──────┬───────┘
           │
     NO ───┴─── YES
     │            │
     ▼            │
┌──────────────────────┐
│ get_host_initiators  │
│ create_host_with_    │
│ initiators.yml       │
└──────────┬───────────┘
           │
           └──────────┐
                      │
                      ▼
           ┌──────────────────────┐
           │ map_volume.yml       │
           └──────────────────────┘
```

### 3. PowerStore Create Host Workflow (NEW)

```
┌─────────────────────────────────────────────────────────────┐
│         POWERSTORE CREATE SINGLE HOST                         │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│ Zoning Workflow      │
│ (roles/zoning)       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ get_host.yml         │
│ (PowerStore)         │
└──────────┬───────────┘
           │
           ▼
    ┌──────────────┐
    │ Host Found?  │
    └──────┬───────┘
           │
     NO ───┴─── YES
     │            │
     ▼            │
┌──────────────────────┐
│ get_host_initiators  │
│ (zoning)             │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ create_host_with_    │
│ initiators.yml       │
│ (PowerStore)         │
└──────────────────────┘
```

### 4. PowerStore Map Volume to Host Workflow (NEW)

```
┌─────────────────────────────────────────────────────────────┐
│         POWERSTORE MAP VOLUME TO HOST                         │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│ get_host.yml         │
│ (PowerStore)         │
└──────────┬───────────┘
           │
           ▼
    ┌──────────────┐
    │ Host Found?  │
    └──────┬───────┘
           │
     NO ───┴─── YES
     │            │
     ▼            │
┌──────────────────────┐
│ FAIL: Host not found │
│ (must create first)  │
└──────────────────────┘
           │
           └──────────┐
                      │
                      ▼
           ┌──────────────────────┐
           │ map_volume.yml       │
           │ (PowerStore)         │
           └──────────────────────┘
```

## Component Relationships

### Storage Platforms Supported
```
┌─────────────────────────────────────────────────────────────┐
│                    STORAGE PLATFORMS                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    Unity     │  │    VPLEX     │  │  PowerStore  │      │
│  │  (Dell EMC)  │  │  (Dell EMC)  │  │  (Dell EMC)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   VMware     │  │    Linux     │  │   Windows    │      │
│  │  (ESXi/vC)   │  │    (SSH)     │  │   (WinRM)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │ Cisco Nexus  │  │  Fibre       │                        │
│  │   Switches   │  │  Channel     │                        │
│  │   (NX-OS)     │  │  Zoning      │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

## New Files Added

### PowerStore Modular Playbooks
1. **playbooks/files/powerstore_create_host.yml**
   - Creates a single host on PowerStore with zoning
   - Similar to unity_map_volume_to_single_host.yml but without volume mapping
   - Enables independent testing of host creation

2. **playbooks/files/powerstore_map_volume_to_host.yml**
   - Maps volume to existing host on PowerStore
   - Assumes host already exists
   - Enables independent testing of volume mapping

3. **roles/powerstore/tasks/map_volume.yml**
   - Task for mapping volumes using dellemc.powerstore.volume module
   - Supports optional HLU (Logical Unit Number)

4. **playbooks/vars/powerstore_create_host_vars.yml**
   - Variables for single host creation
   - Includes: node_hostname, node_type, array_hostname, vcenter

5. **playbooks/vars/powerstore_map_volume_to_host_vars.yml**
   - Variables for volume mapping
   - Includes: node_hostname, array_hostname, vol_name, hlu

## Testing Workflow

### Step 1: Create Host
```bash
ansible-playbook -i playbooks/files/inventory.ini playbooks/files/powerstore_create_host.yml
```
- Runs zoning workflow
- Creates host on PowerStore if not found
- Registers host with FC initiators

### Step 2: Map Volume
```bash
ansible-playbook -i playbooks/files/inventory.ini playbooks/files/powerstore_map_volume_to_host.yml
```
- Verifies host exists
- Maps volume to host
- Fails if host not found (ensures step 1 completed)

## File Statistics
- Total YAML files: 141
- Roles: 6 (common, unity, vmware, vplex, powerstore, zoning)
- Standalone playbooks: 31+
- Custom Python modules: 6
- Filter plugins: 3

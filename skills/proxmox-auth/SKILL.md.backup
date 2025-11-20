# Proxmox Authentication & Management Skill

Expert guidance for Proxmox VE cluster authentication, API access, and infrastructure management.

## Authentication Methods

### SSH Access (Primary)
```bash
# Access Proxmox nodes directly
ssh 192.168.1.100  # spacenode1
ssh 192.168.1.100  # spacenode2

# Execute commands on nodes
ssh 192.168.1.100 "pct list"
ssh 192.168.1.100 "qm list"
```

### Proxmox API via pvesh
```bash
# Get cluster nodes
ssh 192.168.1.100 "pvesh get /nodes"

# Get node status
ssh 192.168.1.100 "pvesh get /nodes/spacenode1/status"

# Get cluster status
ssh 192.168.1.100 "pvecm status"
```

## Cluster Configuration

**Nodes:**
- spacenode1: 192.168.1.100 (4 cores, 11.45 GiB RAM)
- spacenode2: 192.168.1.100 (20 cores, 62.71 GiB RAM)

**Important:** Commands default to the node you're connected to. For cross-node operations, SSH to the target node directly.

## Container Management (LXC)

### Basic Operations
```bash
# List all containers (any node)
ssh 192.168.1.100 "pct list"

# Start container on specific node
ssh 192.168.1.100 "pct start 200"

# Stop container
ssh 192.168.1.100 "pct stop 200"

# Get container status
ssh 192.168.1.100 "pct status 200"

# Execute command in container
ssh 192.168.1.100 "pct exec 200 -- command"
```

### Configuration
```bash
# Read container config
ssh 192.168.1.100 "cat /etc/pve/nodes/spacenode2/lxc/200.conf"

# Find which node hosts a container
ssh 192.168.1.100 "ls -lh /etc/pve/nodes/*/lxc/*.conf | grep 200.conf"
```

### GPU Passthrough Containers
```bash
# CT200 (ai-workloads) on spacenode2
# IP: 192.168.1.100
# Services: Stable Diffusion (7860), ComfyUI (8188), Ollama (11434)

# Access container
ssh root@192.168.1.100

# Check GPU in container
ssh 192.168.1.100 "pct exec 200 -- nvidia-smi"

# Check Docker containers
ssh root@192.168.1.100 "docker ps -a"
```

## VM Management (QEMU)

```bash
# List all VMs
ssh 192.168.1.100 "qm list"

# Start/stop VM
ssh 192.168.1.100 "qm start 100"
ssh 192.168.1.100 "qm stop 100"

# Get VM config
ssh 192.168.1.100 "qm config 100"
```

## Cluster Operations

### Node Information
```bash
# Get all nodes
ssh 192.168.1.100 "pvecm nodes"

# Check cluster status
ssh 192.168.1.100 "pvecm status"

# Get corosync config (node IPs)
ssh 192.168.1.100 "cat /etc/pve/corosync.conf"
```

### Storage
```bash
# List storage
ssh 192.168.1.100 "pvesm status"

# Check specific storage
ssh 192.168.1.100 "pvesm list local-lvm"
```

### Backups
```bash
# List backups
ssh 192.168.1.100 "pvesh get /nodes/spacenode1/storage/local/content --content backup"

# Backup container
ssh 192.168.1.100 "vzdump 200 --mode snapshot --storage local"

# Restore backup
ssh 192.168.1.100 "pct restore 200 /path/to/backup.tar.gz"
```

## Network Diagnostics

### Container Network Issues
```bash
# Check container IP
ssh 192.168.1.100 "pct exec 200 -- ip addr"

# Check if container responds
ping 192.168.1.100

# Test container services
curl -s -o /dev/null -w "%{http_code}" http://192.168.1.100:7860/

# Check container networking from inside
ssh 192.168.1.100 "pct exec 200 -- ip route"
ssh 192.168.1.100 "pct exec 200 -- systemctl status networking"
```

### Bridge Configuration
```bash
# Check bridge status
ssh 192.168.1.100 "ip addr show vmbr0"

# List all bridge connections
ssh 192.168.1.100 "brctl show vmbr0"
```

## Common Patterns

### Find Container Location
```bash
# Search all nodes for container config
ssh 192.168.1.100 "ls -lh /etc/pve/nodes/*/lxc/*.conf | grep -E '200\.conf|VMID|^/'"
```

### Restart Container with Network Reset
```bash
# Stop, wait, start
ssh 192.168.1.100 "pct stop 200 && sleep 5 && pct start 200"

# Check status after restart
ssh 192.168.1.100 "pct status 200"
ping -c 3 192.168.1.100
```

### Check Container Logs
```bash
# System logs
ssh 192.168.1.100 "pct exec 200 -- journalctl -xe"

# Specific service logs
ssh 192.168.1.100 "pct exec 200 -- journalctl -u docker -n 50"
```

## Troubleshooting

### "Configuration file does not exist"
**Cause:** Running command from wrong node (container is on different node)

**Fix:** Find correct node first:
```bash
ssh 192.168.1.100 "ls /etc/pve/nodes/*/lxc/200.conf"
# Result shows: /etc/pve/nodes/spacenode2/lxc/200.conf
# SSH to spacenode2 (192.168.1.100) instead
```

### Container Not Responding on Network
**Checks:**
1. Container running: `ssh 192.168.1.100 "pct status 200"`
2. Has IP: `ssh 192.168.1.100 "pct exec 200 -- ip addr"`
3. Network reachable: `ping 192.168.1.100`
4. Services running: `ssh 192.168.1.100 "pct exec 200 -- systemctl status"`

**Fix:** Restart container or reboot node if needed

### Node Reboots
**After node reboot:**
- Containers with `onboot: 1` start automatically
- Check with: `ssh 192.168.1.100 "pct list | grep running"`
- Manual start if needed: `ssh 192.168.1.100 "pct start 200"`

## Important Notes

- **Always SSH to the correct node** for container operations
- **CT200 is on spacenode2** (192.168.1.100)
- **Use `pct exec`** for running commands inside containers
- **GPU passthrough** requires specific LXC configuration (see CT200 config)
- **DHCP containers** may change IP after restart (check with `pct exec`)

## Quick Reference

| Task | Command |
|------|---------|
| List containers | `ssh NODE "pct list"` |
| Start CT200 | `ssh 192.168.1.100 "pct start 200"` |
| SSH to CT200 | `ssh root@192.168.1.100` |
| Check CT200 status | `ssh 192.168.1.100 "pct status 200"` |
| Get CT200 IP | `ssh 192.168.1.100 "pct exec 200 -- hostname -I"` |
| Check services | `curl http://192.168.1.100:PORT/` |
| Find container node | `ssh 192.168.1.100 "ls /etc/pve/nodes/*/lxc/VMID.conf"` |
| Reboot node | `ssh 192.168.1.100 "reboot"` |

## AI-Workloads Container (CT200)

**Hostname:** ai-workloads
**IP:** 192.168.1.100
**Node:** spacenode2 (192.168.1.100)
**Resources:** 6 cores, 24GB RAM, NVIDIA GPU passthrough

**Services:**
- Stable Diffusion WebUI: http://192.168.1.100:7860
- ComfyUI: http://192.168.1.100:8188
- Ollama: http://192.168.1.100:11434
- Open WebUI: http://192.168.1.100:3000

**Docker Containers:**
```bash
# List all containers
ssh root@192.168.1.100 "docker ps -a"

# Restart services
ssh root@192.168.1.100 "docker restart sd-auto1111"
ssh root@192.168.1.100 "docker restart comfyui"
ssh root@192.168.1.100 "docker restart ollama"
```

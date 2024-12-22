# Hetzner Cloud Server Deployment with Advanced Subnet Selection  

## Project Overview  
This Ansible playbook automates the deployment of servers on Hetzner Cloud, offering:  
- **Precise subnet selection** during server creation – even if multiple subnets exist.  
- **Volume creation and automounting** during deployment.  
- **Cloud-Init support** to personalize server setups.  

### Why This Playbook Stands Out:  
By default, Hetzner Cloud **randomly assigns servers to any available subnet** within a private network, when multiple subnets exists.  
**Hetzner does not allow you to select a specific subnet during server creation.**  

**This playbook solves that limitation.**  
- The user specifies the desired subnet.  
- The playbook calculates the next available IP within that subnet by analyzing:  
  - Existing servers  
  - Load balancers in the subnet  
- The server is then manually assigned the correct IP in the chosen subnet **after creation**, **before start**.  

**Result:**  
- You get the flexibility to deploy servers into specific subnets **without relying on random subnet assignments.**  
- This mirrors the "automatic assignment" behavior that typically happens when only one subnet exists.  
- Because we create the server stopped when adding a specific network and start after attachment, cloud-init is compatible to the specific subnet attachment

---

## Key Features  
- **Subnet Precision** – Attach servers to the exact subnet you need, even when multiple subnets exist.  
- **Next Available IP** – Automatically finds and assigns the next free IP within the subnet.  
- **Volume Support** – Create and attach volumes as part of server provisioning.  
- **Cloud-Init Ready** – Inject custom Cloud-Init configurations during deployment.  

---

## Setup and Installation  

1. Create a project folder and clone this Repo to it

2. Create a Virtual Environment (Recommended)  
python3 -m venv venv  
source venv/bin/activate  

2. Install Required Dependencies  
pip install ansible  
ansible-galaxy collection install hetzner.hcloud  
pip install ipaddress  

3. Set Your Hetzner API Token  
export HCLOUD_TOKEN="your_hetzner_cloud_api_token"  
---

## Running the Playbook  

Basic Deployment  
ansible-playbook deploy_hcloud_server.yml -e server_name=my-server -e server_type=cpx21  

---

## Real-World Use Cases – Example Commands  

1. Standard Server Deployment (No Subnet Selection)  
ansible-playbook deploy_hcloud_server.yml \  
  -e server_name=web-server-1 \  
  -e server_type=cpx21  

2. Deploy a Server with a 10 GB Volume  
ansible-playbook deploy_hcloud_server.yml \  
  -e server_name=db-server \  
  -e server_type=cpx21 \  
  -e volume_size=10  

3. Deploy a Server in a Specific Subnet (10.0.1.0/24)  
ansible-playbook deploy_hcloud_server.yml \  
  -e server_name=app-server \  
  -e server_type=cpx21 \  
  -e subnet=10.0.1.0/24  

4. Combine Subnet and Volume  
ansible-playbook deploy_hcloud_server.yml \  
  -e server_name=multi-node-1 \  
  -e server_type=cpx21 \  
  -e volume_size=20 \  
  -e subnet=10.0.1.0/24  

---

## Comprehensive Variable Breakdown  

+------------------------+-----------------------------------------------------+----------+--------------+--------------------------------------------------+----------------------------+  
| Variable               | Description                                         | Type     | Required     | Dependencies                                     | Default Value              |  
+------------------------+-----------------------------------------------------+----------+--------------+--------------------------------------------------+----------------------------+  
| hcloud_token           | Hetzner Cloud API token                             | String   | Yes          | Must be set in the environment as HCLOUD_TOKEN   | -                          |  
| server_name            | Name of the server to create                        | String   | Yes          | -                                                | example-server             |  
| server_type            | Hetzner server type (e.g., cpx21)                   | String   | Yes          | -                                                | cpx21                      |  
| image                  | OS image (e.g., ubuntu-22.04)                       | String   | No           | -                                                | ubuntu-22.04               |  
| location               | Hetzner location (fsn1, nbg1, hel1)                 | String   | Yes          | -                                                | fsn1                       |  
| ssh_keys               | List of SSH keys                                    | List     | No           | -                                                | []                         |  
| volume_size            | Size of the volume to create (GB)                   | Integer  | No           | -                                                | null                       |  
| volume_name            | Name of the volume                                  | String   | No           | -                                                | server_name-volume         |  
| volume_format          | Filesystem format for the volume                    | String   | No           | -                                                | ext4                       |  
| private_network_name   | Name of the private network                         | String   | No           | -                                                | null                       |  
| private_network_id     | Network ID (auto-detected)                          | String   | No           | Derived from private_network_name                | null                       |  
| subnet                 | Subnet (e.g., 10.0.1.0/24)                          | String   | No           | private_network_name must be defined             | null                       |  
| enable_ipv4            | Enable IPv4                                         | Boolean  | No           | -                                                | true                       |  
| enable_ipv6            | Enable IPv6                                         | Boolean  | No           | -                                                | true                       |  
| cloud_init_file        | Path to Cloud-Init configuration file               | String   | No           | -                                                | cloud-init/cloud-init.yaml |  
+------------------------+-----------------------------------------------------+----------+--------------+--------------------------------------------------+----------------------------+  


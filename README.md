

# Reference Architecture: OpenShift Container Platform on Red Hat Virtualization

This repository contains the Ansible playbooks used to deploy  
an OpenShift Container Platform environment on Red Hat Virtualization.

## Overview

This reference architecture provides a comprehensive example demonstrating how Red Hat OpenShift Container Platform  
can be set up to take advantage of the native high availability capabilities of Kubernetes and Red Hat Virtualization  
in order to create a highly available OpenShift Container Platform environment. Master branch is based on the latest OpenShift version, currently deployed with CNS for dynamic provisioning of Persistent Volumes. By default the installation will deploy Logging, Metrics/Prometheus, Node Exporter, Grafana and a HA-Proxy Loadbalancer for all API and Application traffic with the ability to provide a highly customized OpenShift installation.  This project closely follows the last released reference,  [OpenShift on RHV4](https://access.redhat.com/documentation/en-us/reference_architectures/2017/html-single/deploying_red_hat_openshift_container_platform_3.6_on_red_hat_virtualization_4/).
## Topology

## Virtual Machines
| Hostname | # | vCpus | Memory | Docker disk | Container Disk | Gluster  
| -------- | - | ----- | ------- | ---------- | ---- | ----
| **master#** | 3 | 2 | 4G | 20G vdb | 20G vdc |
| **infra#** | 3 | 2 | 8G | 20G vdb | 20G vdc | 100G vde 
| **node0#** | 2 | 2 | 8G | 20G vdb | 20G vdc |
| **openshift-lb** | 1 | 1 | 4Gb |
| **Totals** | 10 | 19 | 56G | 180G | 180G | 300G

### Nics 
The VMs have hard coded NICS outside the default RHV pool, This makes it easier to reserve in DHCP and DNS if needed.


> master# = master1/2/3
> infra# = infra1/2/3
> node0# = node01/02/03


## Prerequisites
### RHV 
Make sure RHV is installed, [RHV 4.1 Documentation](https://access.redhat.com/documentation/en-us/red_hat_virtualization/?version=4.1)
### Preparing the Deployment Host
**Step 1.**
Git clone the ansible-ocp-rhv repository and run the setup playbook.

```
$ sudo yum install -y git 
$ mkdir -p git
$ cd ~/git/ && git clone https://github.com/hornjason/ansible-ocp-rhv.git
$ cd ~/git/rhev-ocp && ansible-playbook setup.yml
```

Once the playbook has completed your host should be configured with the prerequisites to run the automation.


### Varibles
#### RHV
| Variable | Description
|---|---
| engine_hostname | The hostname of the RHV engine.
| engine_url | Url to engine api. defaults to https://`<engine_hostname>`/ovirt-engine/api.
| engine_user | User to authenticate to RHV.
| engine_password | Password to use for `engine_user`.
| engine_cafile | Certificate Authority file from engine:/etc/pki/ovirt-engine/ca.pem. Path is relative to playbook directory.
| qcow_url | URL to qcow image to upload if needed. Can also be of the form `file:///<path>`.
| rhv_cluster | Name of the RHV cluster to install on.
| rhv_data_center | Name of datacenter to install on.
| rhv_vm_network | VM Network to attach to the Virtual Machines. Defaults to `ovirtmgmt`.
| rhv_data_storage | List of the RHV storage domain to use when creating disks.
#### Virtual Machines
| Variable | Description
|---|---
| template_cluster | Name of RHV cluster to install to. Defaults to `rhv_cluster`
| template_name | Name of the template to clone the virtual machines from.
| template_memory | Amount of memory for the virtual machine. Ex. `4GiB`.
| template_cpu | Number of virtual cores for the virtual machines.
| template_disk_storage | Data storage for the virtual machine to create disks on. Defaults to `rhv_data_storage`.
| template_disk_size | Size of the disk for the provisioned virtual machine. Ex. `30GiB`.
| template_nics | List of NIC's to attach to the virtual machine. Entries should have `name`, `profile_name`, `interface` 
| master_vm_mem | Memory for the master hosts. Ex. `8`.
| master_vm_vcpu | Virtual cpu for the master hosts. Ex. `2`.
| master_docker_volume_size | Size of the docker volume for master hosts in gigabytes. Ex. `10`.
| master_local_volume_size | Size of the local volume for the master hosts in gigabytes. Ex. `10`.
| master_etcd_volume_size | Size of the etcd volume for master hosts in gigabytes. Ex. `10`.
| infra_vm_mem | Memory for the infra hosts. Ex. `8`.
| infra_vm_vcpu | Virtual cpu for the infra hosts. Ex. `2`.
| infra_docker_volume_size | Size of the docker volume for infra hosts in gigabytes. Ex. `10`.
| infra_local_volume_size | Size of the local volume for the infra hosts in gigabytes. Ex. `10`.
| node_vm_mem | Memory for the node hosts. Ex. `8`.
| node_vm_vcpu | Virtual cpu for the node hosts. Ex. `2`.
| node_docker_volume_size | Size of the docker volume for node hosts in gigabytes. Ex. `10`.
| node_local_volume_size | Size of the local volume for the node hosts in gigabytes. Ex. `10`.
#### Subscriptions
| Variable | Description
|---|---
| rhsm_master_key | Activation key for master hosts to use to subscribe to satellite.
| rhsm_master_org | Organization to use for master hosts to use when subscribing to satellite.
| rhsm_node_key | Activation key for node hosts to use to subscribe to satellite.
| rhsm_node_org | Organization to use for node hosts to use when subscribing to satellite.
| rhsm_user | Username to use to subscribe to RHSM. Unnecessary if using activation key.
| rhsm_pass | Password to use to subscribe to RHSM. Unnecessary if using activation key.
| rhsm_broker_pool | Pool id to subscribe masters to. Unnecessary if using activation key.
| rhsm_node_pool | Pool id to subscribe nodes to. Unnecessary if using activation key.
| rhsub_server | Hostname of the subscription server. Ex. `subscription.rhsm.redhat.com`.
| rhsm_satellite | Hostname of the satellite server. Ex. `https://satellite.company.com`.
| rhsm_repos | List of repositories to enable on the hosts.
| rhsm_packages | List of packages to install during cloud-init.
#### Access
| Variable | Description
|---|---
| root_ssh_key | SSH key to add to root's authorized keys list.
#### Openshift
| Variable | Description
|---|---
| console_port | Port to expose the master API on.
| debug_level | Setting the Openshift services Debug output level.
| admin_user | Administrative user to allow through htpasswd auth. Ex. `root`.
| master_nodes | Number of master nodes to provision for the cluster.
| infra_nodes | Number of infra nodes to provision for the cluster.
| app_nodes | Number of app nodes to provision for the cluster.
| lbs | Number of loadbalancers to provision for the cluster.
| public_hosted_zone | The public network zone Openshift components will use. Ex. `cluster1.company.com`.
| local_hosted_zone | The local network zone Openshift components will use. Ex. `cluster1.company.com`.
| apps_dns_prefix | The prefix to use for accessing Openshift application routes. Ex. `apps`.
| load_balancer_hostname | Hostname to access loadbalancer for the master api. Defaults to master.`<local_hosted_zone>`.
| router_cert | Dictionary containing the cafile, certfile, and keyfile to use on the Openshift routers.
| master_cert | Dictionary container the cafiles, certfile, and keyfile to use on the Openshift masters.
| openshift_master_htpasswd_users | Dictionary used to specify user and password for backdoor admin acces using htpasswd.
| openshift_master_identity_providers | Dictionary defining the identity providers to use for authentication to Openshift.
| openshift_disable_check | Disable any health checks performed in the openshift installer pre-flight checks.
| os_sdn_network_plugin_name | Network Plugin name to use for Openshift SDN.
| osm_cluster_network_cidr | CIDR to use to specify IP range for pods/Docker.
| openshift_portal_net | CIDR to use to specify IP range of Openshift Services.
| storage_type | Type of storage to use when installing the cluster. Options are `dynamic` and `none`.
| metrics_volume_size | Size of the persistent volume for metrics storage.
| logging_volume_size | Size of the persistent volume for logging storage.
| prometheus_volume_size | Size of the persistent volume for prometheus storage.
| prometheus_alertmanager_size | Size of the persistent volume for alertmanager storage.
| prometheus_alertbuffer_size | Size of the persistent volume for alertbuffer storage.
| cassandra_volume_size | Size of the persistent volume for cassandra storage.
| registry_volume_size | Size of the persistent volume for registry storage.
| logging_es_size |  Size of the persistent volume for elasticsearch storage.
| logging_es_mem: | Amount of memory to set for Elasticsearch containers. Ex. 16Gi.
| oreg_auth_user | Service account for use with registry.redhat.io.
| oreg_auth_password | Service account password or auth token for use with the auth user.
| openshift_release | Openshift version to use. Ex. "3.11".
| deploy_grafana | Boolean value to deploy Grafana.
| deploy_prometheus | Boolean value to deploy Prometheus.
| deploy_logging | Boolean value to deploy EFK logging stack.
| deploy_metrics | Boolean value to deploy hawkular, heapster, cassandra  metrics stack.
| deploy_ocs | Boolean value to deploy Openshift Container Storage.
| ocs_infra_cluster_usable_storage | Amount of storage usable for to OCS.<TODO>.
| ocs_infra_cluster_allocated_storage |  Amount of storage allocated to OCS. <TODO>.
| ocs_app_cluster_usable_storage | Amount of storage <TODO>.
| container_runtime_docker_storage_setup_device | Device to use for docker storage.
| container_runtime_docker_storage_type | Storage type to use for docker storage. Ex. overlay2.
| oreg_url | Url to use for the Openshift registry components.<TODO>
| openshift_docker_insecure_registries | Registries for docker to allow insecure connections to.
| openshift_docker_blocked_registries | Registries for docker to block access to.
| osm_project_request_message | Message to display when users want to request a project projects.
| local_volumes_device | Device to be used for local volumes on the host. Ex. /dev/vdc.
#### Load Balancer
| Variable | Description
|---|---
<TODO>
### Dynamic Inventory

A copy of `ovirt4.py` from the Ansible project is provided under the inventory directory. This script will, given credentials to a RHV 4 engine, populate the Ansible inventory with facts about all virtual machines in the cluster.

### Red Hat Virtualization Certificate

A copy of the `/etc/pki/ovirt-engine/ca.pem` from the RHV engine will be downloaded using the following variables in `ocp-vars-<env>.yml`.

```
engine_hostname: rhvm.foo.bar
engine_url: "https://{{ engine_hostname }}/ovirt-engine/api"

```

### RHEL QCOW2 Image

The ovirt-ansible role, ovirt-image-template requires a URL to download a QCOW2 KVM image to use as  
the basis for the VMs on which OpenShift will be installed. Using a RHEL image  
is preferred, log in at [https://access.redhat.com/](https://access.redhat.com/), navigate to Downloads, Red Hat Enterprise Linux,  
select the latest release (at this time, 7.5), and copy the URL for “KVM Guest Image”. It is  
preferable to download the image to a local server, e.g. the /pub/ directory of a satellite if  
available, and provide that URL to the Ansible playbook, because the download link will expire  
after a short while and need to be refreshed, or host it locally on a web server thats accessible from the ansible deployment server and update the _qcow_url_ variable in `ocp-vars.yml`  
Ex.  
`qcow_url: http://web.foo.bar:8080/iso/rhel-server-7.4-x86_64-kvm.qcow2
or 
qcow_url: file:///iso/rhel-server-7.4-x86_64-kvm.qcow2`

## Usage

Before running any playbooks its important to specify the environment being built or modified. This is done via an environment varibale. In order to build environment `foo`, the following command must be used to specify this environment:
`export ENV=foo`

This environment variable `ENV`, is used throughout the automation process to tell ansible which variable files to use at runtime. In this case ansible will attempt to source its varibles from `ocp-vars-foo.yml` in the root of the repository. 

The `ENV` varible allows for users of this repository to manage and create multiple Openshift clusters without having to rename and replace name clashing files. Instead, users can simultaneously have many cluster variable files in the root of the repository at once and simply switch between them using the `ENV` varible.

The `ENV` varibale also provides further decoupling of the automation to a specific environment. The only actions that need to be performed for creating a new cluster is a new `ocp-vars-<env>.yml` file to be created and tuned to the users specifications, followed by the setting of the `export ENV=<env>` varible prior to running the automation to select that new cluster.

Edit the `ocp-vars.yml.example` file in this directory, and save it as `ocp-vars-<env>.yml`. Replacing `<env>` with an identifier for your cluster.

VMs are defined in `playbooks/vars/{{ env }}/vars.yml`  
Edit to fit your environment as needed

# Installation

## Virtual Machines + OpenShift

This will deploy all Virtual Machines using `rhev-ocp/playbooks/vars/{{ env }}/vars.yaml`

From the `ansible-ocp-rhv/` directory, run

```
ansible-playbook playbooks/deploy-vms.yaml
ansible-playbook playbooks/openshift-install.yaml -e @ocp-vars-{{ env }}.yml

```

This will provision all VMs and a complete OpenShift infrastructure.

## Manual 2 step Installation

### Virtual machines _ONLY_

From the `ansible-ocp-rhv/` directory, run

```
ansible-playbook playbooks/deploy-vms.yaml -e @ocp-vars-{{ env }}.yml

```

### Set up OpenShift Container Platform on the VMs from the previoius step

```
ansible-playbook playbooks/openshift-install.yaml -e @ocp-vars-{{ env }}.yaml

```



# Reference Architecture: OpenShift Container Platform on Red Hat Virtualization

This repository contains the Ansible playbooks used to deploy  
an OpenShift Container Platform environment on Red Hat Virtualization

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
| Hostname | # | vCpus | Memory | Docker disk | Container Disk | Gluster  
| -------- | - | ----- | ------- | ---------- | ---- | ----
| **master#** | 3 | 2 | 4G | 20G vdb | 20G vdc |
| **infra#** | 3 | 2 | 8G | 20G vdb | 20G vdc | 100G vde 
| **node0#** | 2 | 2 | 8G | 20G vdb | 20G vdc |
| **openshift-lb** | 1 | 1 | 4Gb |
| **Totals** | 10 | 19 | 56G | 180G | 180G | 300G

> master# = master1/2/3
> infra# = infra1/2/3
> node0# = node01/02/03


## Prerequisites
### RHV 
Make sure RHV is installed, [RHV 4.1 Documentation](https://access.redhat.com/documentation/en-us/red_hat_virtualization/?version=4.1)
### Preparing the Deployment Host
**Step 1.**

**deploy-host playbook:**
Ensure the deployment host (aka workstation host) is running Red Hat Enterprise  
Linux 7 and is registered and subscribed to at least the following channels: 

 -   rhel-7-server-rpms
 -   rhel-7-server-extras-rpms
 -   rhel-7-server-ansible-2.4-rpms
 -   ﻿rhel-7-server-rhv-4.1-rpms

`ovirt-ansible-roles` rpm will be installed via the **deploy-host** playbook.

The following commands should be issued from the deployment host (by preference from a  
regular user account with sudo access):

```
$ sudo yum install -y git 
$ mkdir -p ~/git
$ cd ~/git/ && git clone https://github.com/hornjason/rhev-ocp.git
$ cd ~/git/rhev-ocp && ansible-playbook playbooks/deploy-host.yaml -e provider=rhv
```

### Dynamic Inventory

A copy of `ovirt4.py` from the Ansible project is provided under the inventory directory. This script will, given credentials to a RHV 4 engine, populate the Ansible inventory with facts about all virtual machines in the cluster.

### Red Hat Virtualization Certificate

A copy of the `/etc/pki/ovirt-engine/ca.pem` from the RHV engine will be downloaded using the following variables in `ocp-vars.yml`.

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
`qcow_url: http://web.foo.bar:8080/iso/rhel-server-7.4-x86_64-kvm.qcow2`

## Usage

Edit the `ocp-vars.yml` file in this directory, and fill in any blank values.

VMs are defined in `playbooks/vars/ovirt-infra-vars.yaml`  
Edit to fit your environment as needed

# Installation

## Virtual Machines + OpenShift

This will deploy all Virtual Machines using `rhev-ocp/playbooks/vars/ovirt-vm-infra.yaml`

From the `rhev-ocp/` directory, run

```
ansible-playbook playbooks/openshift-install.yaml -e@ocp-vars.yml

```

This will provision all VMs and a complete OpenShift infrastructure.

## Manual 2 step Installation

### Virtual machines _ONLY_

From the `rhev-ocp/` directory, run

```
ansible-playbook playbooks/ovirt-vm-infra.yaml -e@ocp-vars.yml

```

### Set up OpenShift Container Platform on the VMs from the previoius step

```
ansible-playbook playbooks/openshift-install.yaml -e@ocp-vars.yaml

```

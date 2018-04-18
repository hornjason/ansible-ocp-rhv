---


---

<h1 id="reference-architecture--openshift-container-platform-on-red-hat-virtualization">Reference Architecture:  OpenShift Container Platform on Red Hat Virtualization</h1>
<p>This repository contains the Ansible playbooks used to deploy<br>
an OpenShift Container Platform environment on Red Hat Virtualization</p>
<h2 id="overview">Overview</h2>
<p>This reference architecture provides a comprehensive example demonstrating how Red Hat OpenShift Container Platform<br>
can be set up to take advantage of the native high availability capabilities of Kubernetes and Red Hat Virtualization<br>
in order to create a highly available OpenShift Container Platform environment.  Master branch is based on the latest OpenShift version,  currently deployed with CNS for dynamic provisioning of Persistent Volumes.  By default   the installation will deploy Logging, Metrics/Prometheus, Node Exporter, Grafana and a HA-Proxy Loadbalancer for all API and Application traffic with the ability to provide a highly customized OpenShift installation.</p>
<h2 id="prerequisites">Prerequisites</h2>
<h3 id="preparing-the-deployment-host">Preparing the Deployment Host</h3>
<p>Ensure the deployment host (aka workstation host) is running Red Hat Enterprise<br>
Linux 7 and is registered and subscribed to at least the following channels:</p>
<ul>
<li>rhel-7-server-rpms</li>
<li>rhel-7-server-extras-rpms</li>
</ul>
<p>The following commands should be issued from the deployment host (by preference from a<br>
regular user account with sudo access):</p>
<pre><code>$ sudo yum install -y git ansible
$ mkdir -p ~/git
$ cd ~/git/ &amp;&amp; git clone https://github.com/hornjason/rhev-ocp.git
$ cd ~/git/rhev-ocp &amp;&amp; ansible-playbook playbooks/deploy-host.yaml -e provider=rhv
</code></pre>
<h3 id="ovirt-ansible-roles">oVirt Ansible roles</h3>
<p>A copy of the <a href="https://github.com/ovirt/ovirt-ansible">oVirt Ansible</a> repository will be cloned in a directory<br>
alongside this repository. Roles from within the ovirt-ansible repository will be called by playbooks in this one.</p>
<h3 id="dynamic-inventory">Dynamic Inventory</h3>
<p>A copy of <code>ovirt4.py</code> from the Ansible project is provided under the inventory directory. This script will, given credentials to a RHV 4 engine, populate the Ansible inventory with facts about all virtual machines in the cluster.</p>
<h3 id="red-hat-virtualization-certificate">Red Hat Virtualization Certificate</h3>
<p>A copy of the <code>/etc/pki/ovirt-engine/ca.pem</code> from the RHV engine will be downloaded using the following variables in <code>ocp-vars.yml</code>.</p>
<pre><code>engine_hostname: rhvm.foo.bar
engine_url: "https://{{ engine_hostname }}/ovirt-engine/api"
</code></pre>
<h3 id="rhel-qcow2-image">RHEL QCOW2 Image</h3>
<p>The ovirt-ansible role, ovirt-image-template requires a URL to download a QCOW2 KVM image to use as<br>
the basis for the VMs on which OpenShift will be installed.  Using a RHEL image<br>
is preferred, log in at <a href="https://access.redhat.com/">https://access.redhat.com/</a>, navigate to Downloads, Red Hat Enterprise Linux,<br>
select the latest release (at this time, 7.4), and copy the URL for “KVM Guest Image”. It is<br>
preferable to download the image to a local server, e.g. the /pub/ directory of a satellite if<br>
available, and provide that URL to the Ansible playbook, because the download link will expire<br>
after a short while and need to be refreshed, or host it locally on a web server thats accessible from the ansible deployment server and update the <em>qcow_url</em> variable in <code>ocp-vars.yml</code><br>
Ex.<br>
<code>qcow_url: http://web.foo.bar:8080/iso/rhel-server-7.4-x86_64-kvm.qcow2</code></p>
<h2 id="features">Features</h2>
<p>All customization should be handled by one variable file, <code>ocp-vars.yml</code>.   The following details describe features that can be customized for installation and used to generate a new Ansible hosts file.<br>
&lt;&lt; ToDo: &gt;&gt;</p>
<h2 id="usage">Usage</h2>
<p>Edit the <code>ocp-vars.yml</code> file in this directory, and fill in any blank values.</p>
<p>VMs are defined in  <code>playbooks/vars/ovirt-infra-vars.yaml</code><br>
Edit to fit your environment as needed</p>
<p>After installation has completed a OpenShift ansible hosts file will be provided under <code>rhev-ocp/playbooks/inventory/hosts</code>,  providing the ability to run OpenShift playbooks directly later.</p>
<h1 id="installation">Installation</h1>
<h2 id="virtual-machines--openshift">Virtual Machines + OpenShift</h2>
<p>This will deploy all Virtual Machines using <code>rhev-ocp/playbooks/vars/ovirt-vm-infra.yaml</code></p>
<p>From the <code>rhev-ocp/</code> directory, run</p>
<pre><code>ansible-playbook playbooks/openshift-install.yaml -e@ocp-vars.yml
</code></pre>
<p>This will provision all VMs and a complete OpenShift infrastructure.</p>
<h2 id="section"></h2>
<h2 id="manual-2-step-installation">Manual 2 step Installation</h2>
<h3 id="virtual-machines-only">Virtual machines <em>ONLY</em></h3>
<p>From the <code>rhev-ocp/</code> directory, run</p>
<pre><code>ansible-playbook playbooks/ovirt-vm-infra.yaml -e@ocp-vars.yml
</code></pre>
<h3 id="set-up-openshift-container-platform-on-the-vms-from-the-previoius-step">Set up OpenShift Container Platform on the VMs from the previoius step</h3>
<pre><code>ansible-playbook playbooks/openshift-install.yaml -e@ocp-vars.yaml
</code></pre>


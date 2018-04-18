---


---

<h1 id="reference-architecture--openshift-container-platform-on-red-hat-virtualization">Reference Architecture:  OpenShift Container Platform on Red Hat Virtualization</h1>
<p>This repository contains the Ansible playbooks used to deploy<br>
an OpenShift Container Platform environment on Red Hat Virtualization</p>
<h2 id="overview">Overview</h2>
<p>This reference architecture provides a comprehensive example demonstrating how Red Hat OpenShift Container Platform<br>
can be set up to take advantage of the native high availability capabilities of Kubernetes and Red Hat Virtualization<br>
in order to create a highly available OpenShift Container Platform environment.</p>
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
$ cd ~/git/ &amp;&amp; git clone https://github.com/openshift/openshift-ansible-contrib
$ cd ~/git/openshift-ansible-contrib &amp;&amp; ansible-playbook playbooks/deploy-host.yaml -e provider=rhv
</code></pre>
<h3 id="ovirt-ansible-roles">oVirt Ansible roles</h3>
<p>A copy of the <a href="https://github.com/ovirt/ovirt-ansible">oVirt Ansible</a> repository will be cloned in a directory<br>
alongside this repository. Roles from within the ovirt-ansible repository will be called by playbooks in this one.</p>
<h3 id="dynamic-inventory">Dynamic Inventory</h3>
<p>A copy of <code>ovirt4.py</code> from the Ansible project is provided under the inventory directory. This script will, given credentials to a RHV 4 engine, populate the Ansible inventory with facts about all virtual machines in the cluster. In order to use this dynamic inventory, see the <code>ovirt.ini.example</code> file, either providing the relevant Python secrets via environment variables, or by copying it to <code>ovirt.ini</code> and filling in the values.</p>
<h3 id="red-hat-virtualization-certificate">Red Hat Virtualization Certificate</h3>
<p>A copy of the <code>/etc/pki/ovirt-engine/ca.pem</code> from the RHV engine will need to be added to the<br>
<code>reference-architecture/rhv-ansible</code> directory. Replace the example server in the following command to download the certificate:</p>
<pre><code>$ curl --output ca.pem 'http://engine.example.com/ovirt-engine/services/pki-resource?resource=ca-certificate&amp;format=X509-PEM-CA'

</code></pre>
<h3 id="rhel-qcow2-image">RHEL QCOW2 Image</h3>
<p>The ovirt-ansible role, ovirt-image-template requires a URL to download a QCOW2 KVM image to use as<br>
the basis for the VMs on which OpenShift will be installed. If a CentOS image is desired, a suitable<br>
URL is commented out in the variable file, <code>playbooks/vars/ovirt-infra-vars.yaml</code>. If a RHEL image<br>
is preferred, log in at <a href="https://access.redhat.com/">https://access.redhat.com/</a>, navigate to Downloads, Red Hat Enterprise Linux,<br>
select the latest release (at this time, 7.3), and copy the URL for “KVM Guest Image”. It is<br>
preferable to download the image to a local server, e.g. the /pub/ directory of a satellite if<br>
available, and provide that URL to the Ansible playbook, because the download link will expire<br>
after a short while and need to be refreshed.</p>
<h2 id="usage">Usage</h2>
<p>Edit the <code>ocp-vars.yaml</code> file in this directory, and fill in any blank values.</p>
<p>Check variables listed in <code>playbooks/vars/ovirt-infra-vars.yaml</code></p>
<h3 id="set-up-virtual-machines-in-rhv">Set up virtual machines in RHV</h3>
<p>From the <code>reference-architecture/rhv-ansible</code> directory, run</p>
<pre><code>ansible-playbook playbooks/ovirt-vm-infra.yaml -e@ocp-vars.yaml
</code></pre>
<h3 id="set-up-openshift-container-platform-on-the-vms-from-the-previoius-step">Set up OpenShift Container Platform on the VMs from the previoius step</h3>
<pre><code>ansible-playbook playbooks/openshift-install.yaml -e@ocp-vars.yaml
</code></pre>


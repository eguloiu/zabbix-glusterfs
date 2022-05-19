# zabbix-glusterfs
Glusterfs monitoring (including geo-replication and heal info)


gluster-monitoring.py
---------------------
	- This is the main monitoring script
	- Sometimes gluster is busy and responds with an error and that will generate false alerts, in order to fix that the command is repeated up to 3 times
	- Plugin is written for a SINGLE volume - XML output may change for multiple volumes but nowhere to test

ansible_playbook
----------------
	- Contains a role that deploys all the necessary settings on a RedHat based system
	- Tested against RHEL7

zabbix_templates
----------------
	- Contains templates for monitoring various stuff:
		- Template GlusterFS disks.xml - monitors peers status, bricks health, usage, etc
		- Template GlusterFS Heal Info.xml - monitors and alerts on the numbers of entries that need healing
		- Template GlusterFS geo-replication.xml - monitors the geo-replication status

Manual Setup:
-------------
	1. Install python-xmltodict package
	2. Copy ansible_playbook/roles/zabbix_glusterfs/templates/gluster-monitoring.py to /etc/zabbix/gluster-monitoring.py and make it executable (chmot 755 /etc/zabbix/gluster-monitoring.py)
	3. Copy ansible_playbook/roles/zabbix_glusterfs/templates/gluster.conf to /etc/zabbix/zabbix_agentd.d/gluster.conf
	4. Add the necessary permissions to /etc/sudoers
		Cmnd_Alias GLUSTERMON = /etc/zabbix/gluster-monitoring.py *
		Cmnd_Alias GLUSTER = /usr/sbin/gluster
		Defaults:zabbix !requiretty
		Defaults:zabbix !syslog
		zabbix ALL = NOPASSWD: GLUSTER, GLUSTERMON
	5. Restart the zabbix-agent


# README

## How to use Ansible dynamic inventory python script *dyninventory.py* in Ansible.

##### Python Coding : Scott Dozier (scdozier) <scdozier@cisco.com><br>Documentation : Animesh Das (animdas) <animdas@cisco.com><br>The python script and associated files classification : Highly Confidential<br>Date : 08-May-2020  

-----
***dyninventory.py*** is an Ansible dynamic inventory script written in python. This file when used with Ansible or without Ansible will pull CMS customer inventory i.e. hosts from Prod MoM EM7 database.

*The script is tested to work in Python 2.x on CentOS 7.x. Please report if it doesn't work for you.*


#### Following is the dynamic inventory script ***dyninventory.py*** usage example when using with Ansible.

>`$ ansible <HOST/GROUP/PATTERN> -i dyninventory.py --limit <HOST/GROUP/PATTERN> -a "echo $HOSTNAME"`

***\<HOST/GROUP/PATTERN>*** : It is ansible inventory's host, group or pattern(expression) used for targetting. <u>*Check Ansible official documentation about how to build inventory with hosts and groups [here](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#hosts-and-groups), and how to use pattern to target hosts & groups [here](https://docs.ansible.com/ansible/latest/user_guide/intro_patterns.html).*</u>

##### Following are the CMSP component *GROUPS* available through the dynamic inventory script i.e. *dyninventory.py*.

- *For all customer host*: `ALL`

- *Em7 related* : `EM7, EM7DB, EM7PRT, EM7MC, EM7DC, EM7AIO, EM7PRT, EM7DBVIP, EM7GM`
- *Splunk related* : `SPL, SPLDPL, SPLAIO, SPLIND, SPLMAS, SPLSRC`
- *Relay* : `RLY`
- *Linux Jump Servers* : `LNXJMP`
- *Head End* : `HeadEnd`
- *All other*: <u>For customer and all other groups see **List of groups** section [below](#list-of-groups).</u>

#### Example:


1. **Display all *Em7* hosts for customer '*Anthem*'** :
> `$ ansible anthm* -i dyninventory.py --limit EM7 --list-hosts`

2. **Display all *Relay* hosts for customer '*Nomura*'** :
>`$ ansible nomu* -i dyninventory.py --limit RLY --list-hosts`

3. **Display all *Splunk Indexer* hosts for customer '*MetLife*'** :
>`$ ansible metli* -i dyninventory.py --limit SPLIND --list-hosts`

4. **Display all hosts for customer '*Baxter*'** :
>`$ ansible baxt* -i dyninventory.py --list-hosts`

5. **Display all hosts for customer '*Baxter*'** :
>`$ ansible baxt* -i dyninventory.py --list-hosts`

------
### List of groups
#### For list of individual group(customer, component, etc), and host please run the following command:
>`$ python dyninventory.py --list`

The above command will dump *minified(compact) json* with all customer, component, host, etc along with their respective ***group***. e.g. KPN, Anthem, EM7, SPL etc.

#### To convert the ***minified json*** output to ***yaml*** format for easy readability use the command below :

>`$ python dyninventory.py --list | python -c 'import sys, yaml, json; print(yaml.dump(json.loads(sys.stdin.read()), sort_keys=False))'`

**NB: <u>The above command *will not produce ansible compatible yaml* output for use as ansible inventory. This is just given as reference to ease reading of group names for customers, components, etc.**</u>

<br>
That's it.


<br><br><centre>&copy; Owner. All rights reserved.</centre>

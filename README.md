# halo-policy-backup

The script is to backup policies from each module in Halo. It is strongly recommended that you backup your policy before/after making any changes. 

# Steps 
***1.*** Download/Clone this repository to your local machine

***2.*** Edit config.conf

***3.*** Create directory for each module and name the directories "fim", "csm", "firewall", and "lids"

***4.*** Run `python halo-policy-backup.py`

# Requirements and Dependencies

To get started, you must have the following privileges and software resources:

* An active CloudPassage Halo subscription. If you don't have one, Register for CloudPassage to receive your credentials and further instructions by email.
* Access to your CloudPassage API key. Create a new key, with write privileges, specifically for use with this script.
* Python 2.6 or later. 
* If you don't have gitpython installed, please install it via your terminal.
  `pip install gitpython`

<!---
#CPTAGS:community-supported archive
-->

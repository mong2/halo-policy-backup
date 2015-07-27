import api
import os
import os.path
import json
import git
from datetime import datetime

def get_all_policies(host, authtoken, prox):
    conntype = "GET"
    queryurl_csm = "/v1/policies"
    queryurl_fim = "/v1/fim_policies"
    queryurl_fw = "/v1/firewall_policies/"
    queryurl_lids = "/v1/lids_policies/"
    queryurl_SpecialEvent = "/v1/special_events_policies/"
    reqbody = ""

    csm = api.apihit(host, conntype, authtoken, queryurl_csm, reqbody,prox)
    fim = api.apihit(host, conntype, authtoken, queryurl_fim, reqbody,prox)
    fw = api.apihit(host, conntype, authtoken, queryurl_fw, reqbody,prox)
    lids = api.apihit(host, conntype, authtoken, queryurl_lids, reqbody,prox)
    SpecialEvents = api.apihit(host, conntype, authtoken, queryurl_SpecialEvent, reqbody,prox)

    data = {}
    data_csm = []
    data_fim = []
    data_fw = []
    data_lids = []
    data_SpecialEvent = []

    for entry in csm['policies']:
        data_csm.append(entry['id'])

    for entry in fim['fim_policies']:
        data_fim.append(entry['id'])

    for entry in fw['firewall_policies']:
        data_fw.append(entry['id'])

    for entry in lids['lids_policies']:
        data_lids.append(entry['id'])

    for entry in SpecialEvents['special_events_policies']:
        data_SpecialEvent.append(entry['id'])

    data={"csm": data_csm, "fim": data_fim, "fw": data_fw, "lids": data_lids, "se": data_SpecialEvent}


    return data

def get_specific(host, authtoken, prox, savepath,data):
    conntype ="GET"
    reqbody = ""

    dataSpecific = {}
    policy_csm = []
    policy_fim = []
    policy_fw  = []
    policy_lids = []
    policy_se = []
    print "here"
    for i in data['csm']:
        queryurl_csm = "/v1/policies/" + i
        csm = api.apihit(host, conntype, authtoken, queryurl_csm, reqbody,prox)
        name = csm['policy']['name'] + ".json"
        outcome = json.dumps(csm, indent = 2)
        path = savepath + "/csm"
        completename = os.path.join(path, name)
        with open (completename, 'w') as outfile:
            outfile.write(outcome)

    for i in data['fim']:
        queryurl_fim = "/v1/fim_policies/" + i
        fim = api.apihit(host, conntype, authtoken, queryurl_fim, reqbody,prox)
        name = fim['fim_policy']['name'] +".json"
        outcome = json.dumps(csm, indent = 2)
        path = savepath + "/fim"
        completename = os.path.join(path, name)
        with open (completename, 'w') as outfile:
            outfile.write(outcome)

    for i in data['fw']:
        queryurl_fw = "/v1/firewall_policies/" + i
        fw = api.apihit(host, conntype, authtoken, queryurl_fw, reqbody,prox)
        name = fw['firewall_policy']['name'] + ".json"
        outcome = json.dumps(fw, indent = 2)
        path = savepath + "/firewall"
        completename = os.path.join(path, name)
        with open (completename, 'w') as outfile:
            outfile.write(outcome)

    for i in data['lids']:
        queryurl_lids = "/v1/lids_policies/" + i
        lids = api.apihit(host, conntype, authtoken, queryurl_lids, reqbody,prox)
        name = lids['lids_policy']['name'] + ".json"
        outcome = json.dumps(lids, indent = 2)
        path = savepath + "/lids"
        completename = os.path.join(path, name)
        with open (completename, 'w') as outfile:
            outfile.write(outcome)


    # for i in data['se']:
    #     queryurl_SpecialEvent = "/v1/special_events_policies/" + i
    #     se = api.apihit(host, conntype, authtoken, queryurl_SpecialEvent, reqbody,prox)
    #     print se
        # for entry in se['policy']:
        #     name = entry['name']
        # policy_se.append((name, se))

    return "Finished backing up all policies\n " + "Checking if the file is empty or not...."

def localcommit(savepath):
    result = True
    # Write policies to disk
    path_csm = savepath + "/csm"
    path_fim = savepath + "/fim"
    path_fw = savepath + "/firewall"
    path_lids = savepath + "/lids"

    for file in os.listdir(path_csm):
        if os.stat(path_csm + "/" + file).st_size == 0:
            result = False
            print file + " is empty"

    for file in os.listdir(path_fim):
        if os.stat(path_fim + "/" + file).st_size == 0:
            result = False
            print file + " is empty"
    for file in os.listdir(path_fw):
        if os.stat(path_fw + "/" + file).st_size == 0:
            result = False
            print file + "is empty"
    for file in os.listdir(path_lids):
        if os.stat(path_lids + "/" + file).st_size == 0:
            result = False
            print file + " is empty"
    return result

def remotepush(gitrepo, repocomment):
    repo = git.Repo(gitrepo)
    # Make sure we have the lastest version
    repo.git.pull()
    repo.git.add('.')
    if len(repocomment) < 1:
        repo.git.commit(message= "back up at " + str(datetime.now()))
    else:
        repo.git.commit(message = repocomment)
    repo.git.push()
    result = repo.git.status()
    return result

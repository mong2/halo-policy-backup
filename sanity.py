import os


# Returns boolean for path sanity.
def check_path(basepath):
    sane = True
    paths = {}
    # Deleted "special_events, alerts"
    types = ["fim", "csm", "firewall", "lids"]
    bp = str(basepath)
    for t in types:
        paths[t] = bp + "/" + t
    for p in paths:
        if os.path.isdir(paths[p]):
            pass
        else:
            print "Path does not exist: " + paths[p]
            sane = False
        if os.access(paths[p], os.W_OK):
            pass
        else:
            print "Path is not writeable: " + paths[p]
            sane = False
    return(sane)

# Check sanity of config file
def config(fname):
    sane = True
    apihost = ["api.cloudpassage.com", "api.lichi.cloudpassage.com", "api.bass.cloudpassage.com", "api.zink.cloudpassage.com"]
    if fname["api_host"] not in apihost:
        sane = False
    elif fname["api_key"] is None or len(fname["api_key"]) != 8:
        print "Make sure api_key is not empty and should contain 8 characters"
        sane = False
    elif fname["api_secret"] is None or len(fname["api_secret"]) != 32:
        print "Make sure api_secret is not empty and should contain 32 characters"

    if os.path.isdir(fname["repo_base_path"]):
        pass
    else:
        print "Repo path does not exist"
        sane = False
    return(sane)

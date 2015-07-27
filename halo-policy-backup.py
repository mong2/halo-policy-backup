import getopt
import sys
import api
import fn
import sanity



def main(argv):
    # Parse args from CLI
    cli = parse_cli(argv)
    # Dictionary of config items
    config = parse_config(cli)
    # Error Message
    usagetext = ("halo-policy-backup.py -c CONFIGFILE (OPTIONAL)" +
        "Please specify your file name, if not using the default config file\n" +
        "NOTE: Format of config file should follow the default config file\n")

    # Sanity Checks
    # Check if the directory for each policy exist
    directoryexist = sanity.check_path(config["repo_base_path"])
    if directoryexist == False:
        sys.exit("Error message: Please make changes according to above error message")
    # Check the information in config file
    goodconfig = sanity.config(config)
    if goodconfig == False:
        sys.exit("Error message: Please make sure you have filled all the required information in config file")

    # Get API key, set in config structure
    config["auth_token"] = api.get_auth_token(config["api_host"], config["api_key"], config["api_secret"], config["prox"])
    # Get the policy stuff
    infobundle = fn.get_all_policies(config["api_host"], config["auth_token"], config["prox"])
    finalbundle = fn.get_specific(config["api_host"], config["auth_token"],config["prox"], config["repo_base_path"],infobundle)
    # Write files to disk, return bool
    localsuccess = fn.localcommit(config["repo_base_path"])
    if localsuccess == False:
        sys.exit("Error message: Failure to write locally!")
    else:
        print "Updated files written to disk."
        remotesuccess = fn.remotepush(config["repo_base_path"], config["repo_commit_comment"])
        print remotesuccess

def parse_config(cli):
    config = {}
    for opt in cli:
        if opt == "config":
            execfile(cli[opt], config)
    config['prox'] = {'host': config['proxy_host'], 'port': config['proxy_port'] }
    return(config)

def parse_cli(argv):
    cli_stuff = {}
    try:
        opts, args = getopt.getopt(argv, "hc", ["configFile="])
    except:
        print usagetext

    if len(opts) == 0:
        cli_stuff["config"] = "config.conf"
    else:
        for opt, arg in opts:
            if opt == '-h':
                print usagetext
            elif opt in ("-c", "--configFile"):
                cli_stuff["config"] = arg
    print cli_stuff
    return(cli_stuff)

if __name__ == "__main__":
    main(sys.argv[1:])

import os

REMOTE_CONFIG_PATH = "/config/remote"
SSH_CONFIG_PATH = os.path.join(REMOTE_CONFIG_PATH, "ssh_config")
KNOWN_HOSTS_FILE = os.path.join(REMOTE_CONFIG_PATH, "known_hosts")

def remote_cmd(host, cmd):
    ret =  ["/usr/bin/ssh", "-F", SSH_CONFIG_PATH,
            "-o", "UserKnownHostsFile={0:s}".format(KNOWN_HOSTS_FILE),
            "-o", "PasswordAuthentication=no",
            host]
    ret.extend(cmd)
    return ret

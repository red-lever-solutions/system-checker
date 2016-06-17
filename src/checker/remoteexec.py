import os

REMOTE_CONFIG_PATH = "/config/remote"
KNOWN_HOSTS_FILE = os.path.join(REMOTE_CONFIG_PATH, "known_hosts")

def remote_cmd(host, cmd, ssh_config="ssh_config"):
    ssh_config_path = os.path.join(REMOTE_CONFIG_PATH, ssh_config)
    ret =  ["/usr/bin/ssh", "-F", ssh_config_path,
            "-o", "UserKnownHostsFile={0:s}".format(KNOWN_HOSTS_FILE),
            "-o", "PasswordAuthentication=no",
            host]
    ret.extend(cmd)
    return ret

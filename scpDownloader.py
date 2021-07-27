from paramiko import SSHClient
from scp import SCPClient
import paramiko
# read yaml config
import yaml
# alert
import alert


class getRemoteSSHInfo:
    def __init__(self):
        alert.console("INIT", "初始化中...", alert.fontColors.OKBLUE)
        self.loadConfig()
        alert.console("hr", "-----------------", alert.fontColors.OKBLUE)
        self.setSSH()
        alert.console("hr", "-----------------", alert.fontColors.OKBLUE)
        self.scpRemote()
        alert.console("hr", "-----------------", alert.fontColors.OKBLUE)

    def loadConfig(self):
        alert.console("Config", "Loading...", alert.fontColors.WARNING)
        with open("config.yaml", "r") as configYaml:
            self.config = yaml.load(configYaml, Loader=yaml.FullLoader)
        alert.console("Config", "Loading complete!", alert.fontColors.OKGREEN)

    def setSSH(self):
        alert.console("SSH", "waiting for create a ssh connection...",
                      alert.fontColors.WARNING)
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(
            hostname=self.config["ScpConnectInformation"]["Host"],
            username=self.config["ScpConnectInformation"]["UserName"],
            password=self.config["ScpConnectInformation"]["UserPassword"]
        )
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.scp = SCPClient(ssh.get_transport(), sanitize=lambda x: x)
        alert.console("SSH", "Done!", alert.fontColors.OKGREEN)

    def scpRemote(self):
        alert.console("SCP", "Get remote {}'s computer {} file at {}...".format(
            self.config["ScpConnectInformation"]["UserName"],
            self.config["LoaclCorrectFilesPath"]["FileType"],
            self.config["ScpConnectInformation"]["CorrectFilesPath"]),
            alert.fontColors.WARNING
        )
        self.scp.get(remote_path=self.config["ScpConnectInformation"]
                     ["CorrectFilesPath"]+"/*.{}".format(self.config["LoaclCorrectFilesPath"]["FileType"]),
                     local_path=self.config["LoaclCorrectFilesPath"]["Main"]+self.config["LoaclCorrectFilesPath"]["Temp"])
        alert.console("SCP", "Done!", alert.fontColors.OKGREEN)


if __name__ == "__main__":
    remoteComputer = getRemoteSSHInfo()

from streamonitor.manager import Manager
import streamonitor.log as log


class CLIManager(Manager):
    def __init__(self, streamers):
        super().__init__(streamers)
        self.logger = log.Logger("manager_cli")

    def run(self):
        while True:
            line = input("> ")
            reply = self.execCmd(line)
            self.logger.info(reply)

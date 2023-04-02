from allmeca.environments.base import BaseEnvironment


class LocalEnvironment(BaseEnvironment):
    def __init__(self, work_dir):
        self.work_dir = work_dir

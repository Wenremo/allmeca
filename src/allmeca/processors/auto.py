import click

from allmeca.processors.base import Processor
from allmeca.processors import reactions
from allmeca import actions
from allmeca.action_parser import ActionParser


class AutoProcessor(Processor):
    def __init__(self, *, environment, confirm_shell_commands=True):
        self.environment = environment
        self.confirm_shell_commands = confirm_shell_commands

    def process(self, msg):
        actions = self.extract_actions(msg)
        responses = [action.perform(self.environment) for action in actions]
        return reactions.Response("\n\n---\n\n".join(responses))

    def extract_actions(self, msg):
        parser = ActionParser(msg.content, available_actions=available=actions.all)
        return parser.extract_actions()

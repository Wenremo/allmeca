import click

from allmeca.processors.base import Processor
from allmeca.processors import reactions
from allmeca import actions
from allmeca.action_parser import ActionParser
from allmeca.user_interaction import prompt_choice, prompt_line


class AutoProcessor(Processor):
    def __init__(self, *, environment, confirm_actions=True):
        self.environment = environment
        self.confirm_actions = confirm_actions
        self.action_parser = ActionParser(available_actions=actions.all)

    def process(self, msg):
        actions = self.extract_actions(msg)
        if len(actions) == 0:
            yield from self.process_no_actions(msg)
        else:
            yield from self.process_actions(actions)

    def process_no_actions(self, msg):
        reply = prompt_choice(
            "No actions found in message. Continue?",
            y="yes",
            n="no",
            o="Give a new objective",
        )
        if reply == "y":
            yield reactions.Noop()
        elif reply == "o":
            objective = prompt_line("New objective")
            yield reactions.Response(f"Your new objective is: {objective}")
        else:
            yield reactions.Stop()

    def process_actions(self, actions):
        for action in actions:
            if action.is_valid():
                if self.confirm_actions:
                    reply = ""
                    while reply not in ["y", "n"]:
                        reply = click.prompt(
                            f"Perform action: {action.summary()}? [y/n/?]"
                        ).lower()
                        if reply == "?":
                            click.echo("The full action is:\n")
                            click.echo(str(action))
                            click.echo()
                    if reply == "n":
                        yield reactions.Response(
                            f"Action not allowed by user: {action.summary()}"
                        )
                        continue

                output = action.perform(self.environment)
                yield reactions.Response(output)
            else:
                output = ["Invalid action: {}".format(action.summary())]
                output.extend([f"  - {error}" for error in action.errors])
                output = "\n".join(output)
                yield reactions.Response(output)

    def extract_actions(self, msg):
        return self.action_parser.extract_actions(msg.content)

import click

from allmeca.processors.base import Processor
from allmeca.processors import reactions


class HumanProcessor(Processor):
    def process(self, msg):
        click.echo("Please perform any commands given below:\n")
        click.echo(msg.content)
        click.echo("\n")
        click.echo("Paste the response to the bot, or type /exit to stop")
        response = click.edit()
        if response is None:
            return reactions.Noop()
        response = response.strip()
        if response == "/exit":
            return reactions.Stop()
        else:
            return reactions.Response(response)

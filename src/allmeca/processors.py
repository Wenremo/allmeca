import click


class Processor:
    pass


class HumanProcessor(Processor):
    def process(self, msg):
        click.echo("Please perform any commands given below:\n")
        click.echo(msg.content)
        click.echo("\n")
        click.echo("Paste the response to the bot, or type /exit to stop")
        response = click.edit().strip()
        if response == "/exit":
            exit(0)
        else:
            return response

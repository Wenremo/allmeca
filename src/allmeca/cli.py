import click

from allmeca.bot import MainBot
from allmeca.processors import HumanProcessor


@click.command()
@click.option("--model", default="gpt-3.5-turbo")
@click.argument("task")
def main(model, task):
    processor = HumanProcessor()
    bot = MainBot(processor=processor, model=model)
    bot.run(task)


if __name__ == "__main__":
    main()

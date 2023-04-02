import click
from pathlib import Path

from allmeca.bot import MainBot
from allmeca.processors.human import HumanProcessor
from allmeca.processors.auto import AutoProcessor
from allmeca import environments
from allmeca.prompts import load_prompt_set
from allmeca.messages import NullPersistence, FilePersistence


@click.command()
@click.option("--model", default="gpt-3.5-turbo")
@click.option("--prompt-set", default="default")
@click.option("--history-path", default=None)
@click.option("--work-dir", type=Path, required=True)
@click.argument("task")
def main(model, prompt_set, task, history_path, work_dir):
    if history_path is None:
        persistence = NullPersistence()
    else:
        persistence = FilePersistence(history_path)

    environment = environments.LocalEnvironment(work_dir=work_dir)
    processor = AutoProcessor(environment=environment)
    prompt_set = load_prompt_set(prompt_set)
    bot = MainBot(
        processor=processor, model=model, prompt_set=prompt_set, persistence=persistence
    )
    bot.run(task)


if __name__ == "__main__":
    main()

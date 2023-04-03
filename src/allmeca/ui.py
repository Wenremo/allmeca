import click
from emoji import emojize


_CHOICE_USE_GET_CHAR = True


def info_style(s):
    return click.style(s, fg="cyan")


def prompt_style(s):
    return click.style(s, fg="magenta", bold=True)


def prompt_format(s):
    return emojize(":red_question_mark: ") + prompt_style(s)


def info(s, emoji="information"):
    click.echo(emojize(f":{emoji}: ") + info_style(s))


def prompt_choice(text, only_key=True, **choices):
    keys = set(choices.keys())
    keys_str = "/".join(choices.keys())
    while True:
        if _CHOICE_USE_GET_CHAR:
            assert all(len(key) == 1 for key in keys)
            click.echo(prompt_format(f"{text} [{keys_str}/?]") + ": ", nl=False)
            choice = click.getchar()
            click.echo(choice)
        else:
            choice = (
                click.prompt(prompt_format(f"{text} [{keys_str}/?]")).lower().strip()
            )
        if choice in keys:
            return choice

        for key, value in choices.items():
            click.echo(f"{key}: {value}")


def prompt_yesno(text):
    return prompt_choice(text, y="yes", n="no") == "y"


def prompt_line(text, default=None):
    return click.prompt(prompt_format(text), default=default)


def edit_text(text=""):
    edited = click.edit(text)
    if edited is None:
        return text
    else:
        return edited


if __name__ == "__main__":
    info("Hello world!")
    prompt_yesno("Do you like it?")

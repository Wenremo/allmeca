import click


_CHOICE_USE_GET_CHAR = True


def prompt_style(s):
    return click.style(s, fg="magenta", bold=True)


def prompt_choice(text, only_key=True, **choices):
    keys = set(choices.keys())
    keys_str = "/".join(choices.keys())
    while True:
        if _CHOICE_USE_GET_CHAR:
            assert all(len(key) == 1 for key in keys)
            click.echo(prompt_style(f"{text} [{keys_str}/?]") + ": ", nl=False)
            choice = click.getchar()
            click.echo()
        else:
            choice = (
                click.prompt(prompt_style(f"{text} [{keys_str}/?]")).lower().strip()
            )
        if choice in keys:
            return choice

        for key, value in choices.items():
            click.echo(f"{key}: {value}")


def prompt_line(text, default=None):
    return click.prompt(prompt_style(text), default=default)


def edit_text(text=""):
    edited = click.edit(text)
    if edited is None:
        return text
    else:
        return edited

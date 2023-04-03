import click


def prompt_choice(text, **choices):
    keys = set(choices.keys())
    keys_str = "/".join(choices.keys())
    while True:
        choice = click.prompt(f"{text} [{keys_str}/?]").lower()
        if choice in keys:
            return choice

        for key, value in choices.items():
            click.echo(f"{key}: {value}")


def prompt_line(text, default=None):
    return click.prompt(text, default=default)


def edit_text(text=""):
    edited = click.edit(text)
    if edited is None:
        return text
    else:
        return edited

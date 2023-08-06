import click
from termcolor import colored
import io


@click.command()
@click.argument('filename', required=True, nargs=-1)
def dog(filename):
    for file in filename:
        try:
            click.echo(colored("(", 'red') + colored(file, 'green') + colored(")", 'red'))
            with io.open(file, "r", encoding="unicode-escape") as rv:
                click.echo(colored(rv.read(), 'blue'))
        except FileNotFoundError:
            click.echo(colored("File not found", 'red'))

        except PermissionError:
            click.echo(colored("Permission denied", 'red'))
        except Exception as e:
            click.echo(colored(f"{e}", 'red'))

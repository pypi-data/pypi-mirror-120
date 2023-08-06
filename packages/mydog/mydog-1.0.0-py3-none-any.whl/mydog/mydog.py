import click
from termcolor import colored


@click.command()
@click.argument('filename', required=True, nargs=-1)
def dog(filename):
    for file in filename:
        click.echo(colored("(", 'red') + colored(file, 'green')+colored(")", 'red') )
        with open(file, 'r') as rv:
            click.echo(colored(rv.read(), 'blue'))

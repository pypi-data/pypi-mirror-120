import click
from click.decorators import command

@click.command()
def test():
    with open("/home/cliadmin/cron_test/test.txt", "a") as file:
        file.write("hi" + "\n")
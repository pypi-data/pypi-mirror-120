import click
from click.decorators import command
import os

@click.command()
def test():
    path = os.getenv.get('file_path')
    with open(f"{path}/test.txt", "a") as file:
        file.write("hi" + "\n")
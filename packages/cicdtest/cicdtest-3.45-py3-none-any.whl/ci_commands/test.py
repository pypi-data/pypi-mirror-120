import click
from click.decorators import command
import os

@click.command()
def test():
    path = os.getenv('file_path')
    print(path)
    with open(f"{path}/test.txt", "a") as file:
        file.write("hi" + "\n")
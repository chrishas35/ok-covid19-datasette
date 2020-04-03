import os
from glob import glob

import click

from extract_util import get_contents


@click.command()
# @click.argument("pdf", type=click.Path(exists=True))
@click.option("--input", "-i", type=click.Path(exists=True, readable=True))
@click.option(
    "--output-dir",
    default="test-data/",
    type=click.Path(exists=True, file_okay=False, writable=True),
)
@click.option("--echo", default=False)
def main(input, output_dir, echo):
    if os.path.isfile(input):
        file_list = [input]
    else:
        file_list = glob(f"{input}/*.pdf")

    for i in file_list:
        filename = os.path.join(output_dir, i.split("/")[-1].replace(".pdf", ".txt"))
        generate(i, filename, echo)


def generate(pdf, dest, echo):
    contents = get_contents(pdf)

    if echo:
        print(contents)
        return

    with open(dest, "w") as f:
        f.write(contents)


if __name__ == "__main__":
    main()

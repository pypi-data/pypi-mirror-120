"""Console script for bk."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for bk."""
    click.echo("Starting bookmarks...")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

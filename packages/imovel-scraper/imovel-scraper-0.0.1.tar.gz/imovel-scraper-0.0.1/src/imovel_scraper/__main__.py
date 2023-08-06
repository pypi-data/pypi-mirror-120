"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Imovel Scraper."""


if __name__ == "__main__":
    main(prog_name="imovel-scraper")  # pragma: no cover

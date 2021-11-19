import click


@click.group()
def cli():
    """Welcome the to cli for managing Server"""
    pass


@click.command()
def initdb():
    from server import engine
    from joshBack.models import createTables

    createTables(engine)
    click.echo("Initialized the database")


@click.command()
def dropdb():
    from server import engine
    from joshBack.models import destroyTables

    destroyTables(engine)
    click.echo("Dropped the database")


@click.command()
def migrate():
    from flask_migrate import Migrate, MigrateCommand
    from flask_script import Manager
    from server import app, SQLSession

    session = SQLSession()
    manager = Manager(app)
    migrate = Migrate(app, session)
    manager.add_command("db", MigrateCommand)


cli.add_command(initdb)
cli.add_command(dropdb)
cli.add_command(migrate)


if __name__ == "__main__":
    cli()

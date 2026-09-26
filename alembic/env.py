"""
    Choses a faire:
        - import les settings 
        - import Base 
        - import les models 
        - target_metadata = Base.metadata 
        - Bien changer le prefix:  config.set_main_option(
        'sqlalchemy.url',
        settings.get_db_url.replace('postgresql+asyncpg', 'postgresql+psycopg'),
        )
        - coller la meme chose au debut de run_migration_online()



    Pour faire les migrations:
        - generer une migration: `alembic revision --autogenerate -m 'your message' : attention ca genere le script mais ne l'applique pas !
        - appliquer la migration: `alembic upgrade head`

"""


from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# IMPORT TO DO  ===================================================================
# the settings
from app.core.settings import settings 
# the Base models 
from app.core.database import Base 
# all models 
from app.users.models import User 

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# MODIFY PATH HERE  ----------------------------------------------------
config.set_main_option(
        'sqlalchemy.url',
        settings.get_db_url.replace('postgresql+asyncpg', 'postgresql+psycopg'),
        )


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# ADD BASE metadata -----------------------------------------------------
target_metadata = Base.metadata 

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


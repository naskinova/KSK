from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# ✅ Import your Base and models so Alembic can detect them
from app.database.base import Base
from app.auth import models  # 👈 This line makes Alembic aware of User
from app.auth.models import User
from app.grades.models import Grade

from app.config import settings

# Alembic Config
config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Set model metadata for autogenerate
target_metadata = Base.metadata

# --- Migrations in Offline Mode ---
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# --- Migrations in Online Mode ---
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# ✅ Run the correct mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

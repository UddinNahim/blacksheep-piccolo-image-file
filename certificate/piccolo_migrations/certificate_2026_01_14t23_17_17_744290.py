from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Boolean
from piccolo.columns.indexes import IndexMethod


ID = "2026-01-14T23:17:17:744290"
VERSION = "1.30.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="certificate", description=DESCRIPTION
    )

    manager.add_column(
        table_class_name="Certificate",
        tablename="certificate",
        column_name="is_active",
        db_column_name="is_active",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": True,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    return manager

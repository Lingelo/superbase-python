"""Script to apply database migrations to Supabase."""
import asyncio
from pathlib import Path

from supabase import create_client

from src.chatbot.infrastructure.config import settings


async def apply_migrations() -> None:
    """Apply all SQL migrations to Supabase."""
    client = create_client(settings.supabase_url, settings.supabase_key)

    migrations_dir = Path(__file__).parent.parent / "migrations"
    migration_files = sorted(migrations_dir.glob("*.sql"))

    print(f"Found {len(migration_files)} migration files")

    for migration_file in migration_files:
        print(f"\nApplying migration: {migration_file.name}")

        with open(migration_file, "r") as f:
            sql_content = f.read()

        try:
            # Execute the SQL using the REST API
            # Note: This uses the Supabase RPC functionality
            # For production, consider using a proper migration tool
            result = client.rpc("exec_sql", {"sql": sql_content}).execute()
            print(f"✓ Successfully applied {migration_file.name}")
        except Exception as e:
            print(f"✗ Error applying {migration_file.name}: {str(e)}")
            print(
                "\nPlease apply migrations manually through the Supabase dashboard SQL Editor."
            )
            print(f"SQL content from {migration_file.name}:")
            print("-" * 80)
            print(sql_content)
            print("-" * 80)


if __name__ == "__main__":
    print("=" * 80)
    print("Supabase Migration Tool")
    print("=" * 80)
    print("\nNote: This script requires manual migration application.")
    print(
        "Please go to your Supabase dashboard > SQL Editor and run each migration file.\n"
    )

    migrations_dir = Path(__file__).parent.parent / "migrations"
    migration_files = sorted(migrations_dir.glob("*.sql"))

    for i, migration_file in enumerate(migration_files, 1):
        print(f"\n{i}. {migration_file.name}")
        print(f"   Path: {migration_file}")

    print("\n" + "=" * 80)
    print(
        "After applying migrations, you can test the API with the following endpoints:"
    )
    print("  - POST /api/v1/conversations (Create a new conversation)")
    print("  - GET  /api/v1/conversations (List all conversations)")
    print("  - POST /api/v1/conversations/{id}/messages (Send a message)")
    print("  - GET  /api/v1/conversations/{id}/messages (Get conversation messages)")
    print("=" * 80)

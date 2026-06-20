import asyncio
import asyncpg
import os

POSTGRES_URL = os.getenv("DATABASE_URL", "postgresql://agentwatch:agentwatchpassword@localhost:5432/agentwatch")

# Convert asyncpg to standard format if needed (e.g. postgresql+asyncpg:// -> postgresql://)
if POSTGRES_URL.startswith("postgresql+asyncpg://"):
    POSTGRES_URL = POSTGRES_URL.replace("postgresql+asyncpg://", "postgresql://")

async def init_db():
    print("Connecting to database...")
    conn = await asyncpg.connect(POSTGRES_URL)
    try:
        print("Reading postgres_schema.sql...")
        with open("postgres_schema.sql", "r") as f:
            schema = f.read()
        print("Executing schema...")
        await conn.execute(schema)
        print("Database initialization complete.")
    except Exception as e:
        print(f"Error initializing DB: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(init_db())

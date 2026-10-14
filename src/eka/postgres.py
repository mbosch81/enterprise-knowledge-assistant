"""Parameterized, tenant-filtered pgvector adapter for the offline embedding baseline."""
import psycopg
from eka.core import Chunk, DIM, embed

class PostgresStore:
    def __init__(self, dsn):
        self.dsn = dsn
        with psycopg.connect(dsn) as conn:
            conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
            conn.execute(f"CREATE TABLE IF NOT EXISTS chunks (id text PRIMARY KEY, tenant text NOT NULL, source text NOT NULL, location text NOT NULL, content text NOT NULL, embedding vector({DIM}) NOT NULL)")
    def upsert(self, chunks):
        with psycopg.connect(self.dsn) as conn:
            for c in chunks:
                conn.execute("INSERT INTO chunks VALUES (%s,%s,%s,%s,%s,%s::vector) ON CONFLICT(id) DO NOTHING", (c.id,c.tenant,c.source,c.location,c.text,str(embed(c.text))))
    def search(self, tenant, question, limit=3):
        with psycopg.connect(self.dsn) as conn:
            rows = conn.execute("SELECT 1-(embedding <=> %s::vector),id,tenant,source,location,content FROM chunks WHERE tenant=%s ORDER BY embedding <=> %s::vector,id LIMIT %s", (str(embed(question)),tenant,str(embed(question)),limit)).fetchall()
        return [(row[0],Chunk(*row[1:])) for row in rows]

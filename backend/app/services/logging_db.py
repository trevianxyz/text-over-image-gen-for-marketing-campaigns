"""Campaign logging to DuckDB"""
import duckdb
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# Database file location (will be mounted via Docker volume)
DB_PATH = Path("db/campaigns.duckdb")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Connection pool (reuse connections)
_conn: Optional[duckdb.DuckDBPyConnection] = None

def get_connection() -> duckdb.DuckDBPyConnection:
    """Get or create a connection to DuckDB"""
    global _conn
    if _conn is None:
        _conn = duckdb.connect(str(DB_PATH))
    return _conn

def init_db():
    """Initialize the DuckDB tables - called on app startup"""
    try:
        conn = get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS campaigns (
                campaign_id VARCHAR PRIMARY KEY,
                created_at TIMESTAMP,
                products VARCHAR,
                region VARCHAR,
                audience VARCHAR,
                message TEXT,
                output_square VARCHAR,
                output_landscape VARCHAR,
                output_portrait VARCHAR,
                compliance_status VARCHAR,
                compliance_issues TEXT
            )
        """)
        print("✅ DuckDB initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize DuckDB: {e}")
        raise

def close_db():
    """Close the DuckDB connection - called on app shutdown"""
    global _conn
    if _conn is not None:
        try:
            _conn.close()
            _conn = None
            print("✅ DuckDB connection closed")
        except Exception as e:
            print(f"❌ Error closing DuckDB: {e}")

def log_campaign(campaign_id: str, brief: Any, outputs: Dict[str, str], compliance: Dict) -> None:
    """Log campaign data to DuckDB"""
    try:
        conn = get_connection()
        
        conn.execute("""
            INSERT INTO campaigns VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            campaign_id,
            datetime.now(),
            str(brief.products),
            brief.region,
            brief.audience,
            brief.message,
            outputs.get("1:1", ""),
            outputs.get("16:9", ""),
            outputs.get("9:16", ""),
            compliance.get("status", "unknown"),
            str(compliance.get("issues", []))
        ])
        
        print(f"✅ Logged campaign {campaign_id} to DuckDB")
    except Exception as e:
        print(f"❌ Failed to log campaign {campaign_id}: {e}")
        # Don't raise - logging failure shouldn't break the API response
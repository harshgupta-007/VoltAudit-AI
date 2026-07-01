"""SQLite database configuration and master data seeding for VoltAudit MCP."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "voltaudit.db"


def get_connection() -> sqlite3.Connection:
    """Open and return a connection to the SQLite database.

    Returns:
        sqlite3.Connection object.
    """
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize SQLite database tables and seed canonical master data."""
    conn = get_connection()
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Vendors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendors (
            id TEXT PRIMARY KEY,
            canonical_name TEXT UNIQUE NOT NULL,
            tax_id TEXT NOT NULL,
            address TEXT
        );
    """)

    # 2. Contracts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contracts (
            id TEXT PRIMARY KEY,
            vendor_id TEXT NOT NULL,
            contract_number TEXT UNIQUE NOT NULL,
            effective_date TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            payment_terms_days INTEGER NOT NULL,
            max_authorized_amount REAL NOT NULL,
            capacity_charge_rate REAL NOT NULL,
            variable_charge_rate REAL NOT NULL,
            peak_rate_multiplier REAL NOT NULL,
            FOREIGN KEY (vendor_id) REFERENCES vendors (id)
        );
    """)

    # 3. Purchase Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchase_orders (
            id TEXT PRIMARY KEY,
            po_number TEXT UNIQUE NOT NULL,
            allocated_funds REAL NOT NULL,
            consumed_funds REAL NOT NULL
        );
    """)

    # 4. Meter Readings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meter_readings (
            id TEXT PRIMARY KEY,
            meter_id TEXT NOT NULL,
            reading_date TEXT NOT NULL,
            total_generation_mwh REAL NOT NULL
        );
    """)

    # 5. Invoices table (for historical checks)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id TEXT PRIMARY KEY,
            vendor_id TEXT,
            invoice_number TEXT NOT NULL,
            invoice_date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (vendor_id) REFERENCES vendors (id)
        );
    """)

    # 6. Audit Runs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_runs (
            id TEXT PRIMARY KEY,
            invoice_id TEXT NOT NULL,
            executed_at TEXT NOT NULL,
            compliance_score INTEGER NOT NULL,
            outcome TEXT NOT NULL
        );
    """)

    # 7. Discrepancies table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS discrepancies (
            id TEXT PRIMARY KEY,
            audit_run_id TEXT NOT NULL,
            type TEXT NOT NULL,
            severity TEXT NOT NULL,
            description TEXT NOT NULL,
            expected_value TEXT,
            actual_value TEXT,
            FOREIGN KEY (audit_run_id) REFERENCES audit_runs (id)
        );
    """)

    conn.commit()

    # Seed master data if vendors table is empty
    cursor.execute("SELECT COUNT(*) FROM vendors;")
    if cursor.fetchone()[0] == 0:
        # Seed Vendors
        cursor.execute(
            "INSERT INTO vendors VALUES (?, ?, ?, ?);",
            ("vendor-001-google", "Google LLC", "US-1234567", "1600 Amphitheatre Pkwy"),
        )
        cursor.execute(
            "INSERT INTO vendors VALUES (?, ?, ?, ?);",
            ("vendor-002-chevron", "Chevron Corp", "US-9876543", "6001 Bollinger Canyon Rd"),
        )

        # Seed Contracts
        cursor.execute(
            "INSERT INTO contracts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
            (
                "contract-001",
                "vendor-001-google",
                "CON-GOOGLE-2026",
                "2026-01-01",
                "2026-12-31",
                30,
                1000000.0,
                120.0,
                0.05,
                1.5,
            ),
        )
        cursor.execute(
            "INSERT INTO contracts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
            (
                "contract-002",
                "vendor-002-chevron",
                "CON-CHEVRON-2026",
                "2026-01-01",
                "2026-06-30",
                45,
                500000.0,
                150.0,
                0.08,
                1.2,
            ),
        )

        # Seed Purchase Orders
        cursor.execute(
            "INSERT INTO purchase_orders VALUES (?, ?, ?, ?);",
            ("po-001", "PO-2026-909", 50000.0, 12000.0),
        )

        # Seed Meter Readings
        cursor.execute(
            "INSERT INTO meter_readings VALUES (?, ?, ?, ?);",
            ("reading-001", "MET-WINDFARM-01", "2026-06-30", 1250.45),
        )

        # Seed Historical Invoices
        cursor.execute(
            "INSERT INTO invoices VALUES (?, ?, ?, ?, ?);",
            ("hist-inv-001", "vendor-001-google", "INV-2026-909", "2026-05-15", 1080.0),
        )

        conn.commit()

    conn.close()


if __name__ == "__main__":
    init_db()

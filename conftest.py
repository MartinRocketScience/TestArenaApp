import os
import re
from pathlib import Path

import chromedriver_autoinstaller
import mysql.connector
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService

# Load environment variables
load_dotenv()


def execute_sql_file(cursor, sql_file_path):
    """Execute SQL file with proper handling of delimiters for triggers"""
    with open(sql_file_path, "r", encoding="utf-8") as file:
        # Read the entire file
        sql_content = file.read()

        # Split on DELIMITER commands
        parts = re.split(r"(?i)DELIMITER\s*(\S+)", sql_content)

        current_delimiter = ";"

        for i in range(0, len(parts), 2):
            sql_part = parts[i]
            next_delimiter = parts[i + 1] if i + 1 < len(parts) else None

            if not sql_part.strip():
                continue

            # Split statements based on current delimiter
            statements = sql_part.split(current_delimiter)

            # Execute each statement
            for statement in statements:
                if statement.strip():
                    try:
                        cursor.execute(statement)
                    except mysql.connector.Error as e:
                        print(f"Error executing SQL: {e}")
                        print(
                            f"Statement: {statement[:200]}..."
                        )  # Print first 200 chars
                        raise

            if next_delimiter:
                current_delimiter = next_delimiter


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Initialize test database before running tests"""
    print("\nSetting up test database...")

    try:
        # Connect to database
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        cursor = connection.cursor()

        # Get all tables from the database
        cursor.execute(
            """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = %s
        """,
            (os.getenv("DB_NAME"),),
        )

        existing_tables = [table[0] for table in cursor.fetchall()]

        if existing_tables:
            print(f"Found existing tables: {', '.join(existing_tables)}")
            print("Dropping all existing tables...")

            # Disable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

            # Drop all existing tables
            for table in existing_tables:
                cursor.execute(f"DROP TABLE IF EXISTS `{table}`")
                print(f"Dropped table: {table}")

            # Re-enable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            connection.commit()
            print("All existing tables dropped")

        # Read and execute SQL file to create fresh tables
        print("Creating new tables...")
        sql_file_path = Path(__file__).parent / "test_data" / "test_db_data.sql"

        # Execute SQL file with proper handling of delimiters
        execute_sql_file(cursor, sql_file_path)
        connection.commit()
        print("Test database initialized with fresh data")

        yield

    except Exception as e:
        print(f"Error setting up test database: {str(e)}")
        raise
    finally:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals():
            connection.close()
        print("\nDatabase connections closed")


@pytest.fixture(scope="session", autouse=True)
def config():
    """Configuration for tests"""
    pytest.config = {
        "base_url": os.getenv("BASE_URL"),
        "browser": os.getenv("BROWSER"),
        "headless": os.getenv("HEADLESS"),
        "implicit_wait": os.getenv("IMPLICIT_WAIT"),
        "explicit_wait": os.getenv("EXPLICIT_WAIT"),
    }
    return pytest.config


@pytest.fixture(autouse=True)
def driver(config):
    """Setup webdriver for tests"""
    browser = config["browser"].lower()

    if browser == "chrome":
        # Install ChromeDriver if needed
        chromedriver_autoinstaller.install()

        options = webdriver.ChromeOptions()
        if config["headless"]:
            options.add_argument("--headless")

        pytest.driver = webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if config["headless"]:
            options.add_argument("--headless")
        pytest.driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    pytest.driver.implicitly_wait(config["implicit_wait"])

    yield pytest.driver

    pytest.driver.quit()
    del pytest.driver

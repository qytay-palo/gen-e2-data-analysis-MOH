"""
Database Connector Module for MOH Polyclinic Data Extraction
Version: 1.0
Created: 2026-01-26

This module provides database connection management with:
- Multiple database support (PostgreSQL, MySQL, MSSQL, Oracle)
- Connection pooling
- Retry logic
- Secure credential management
- Query execution with timeout handling
"""

import os
import logging
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import yaml
import psycopg2
from psycopg2 import pool
import pymysql
import pyodbc
import cx_Oracle
from contextlib import contextmanager


logger = logging.getLogger(__name__)


class DatabaseConnector:
    """
    Manages database connections for data extraction.
    Supports PostgreSQL, MySQL, MS SQL Server, and Oracle.
    """
    
    def __init__(self, config_path: str = 'config/database.yml'):
        """
        Initialize database connector with configuration.
        
        Args:
            config_path: Path to database configuration file
        """
        self.config = self._load_config(config_path)
        self.connection_pools = {}
        self._initialize_pools()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load database configuration from YAML file."""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Substitute environment variables
        return self._substitute_env_vars(config)
    
    def _substitute_env_vars(self, config: Dict) -> Dict:
        """Replace environment variable placeholders with actual values."""
        if isinstance(config, dict):
            return {k: self._substitute_env_vars(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [self._substitute_env_vars(item) for item in config]
        elif isinstance(config, str) and config.startswith('${') and config.endswith('}'):
            env_var = config[2:-1]
            return os.getenv(env_var, config)
        return config
    
    def _initialize_pools(self):
        """Initialize connection pools for all configured databases."""
        for db_name, db_config in self.config['databases'].items():
            try:
                db_type = db_config.get('type', 'postgresql')
                pool_size = db_config.get('pool_size', 5)
                
                if db_type == 'postgresql':
                    self.connection_pools[db_name] = self._create_postgres_pool(
                        db_config, pool_size
                    )
                elif db_type == 'mysql':
                    # MySQL doesn't have built-in pooling, use simple connection
                    self.connection_pools[db_name] = db_config
                elif db_type in ['mssql', 'sqlserver']:
                    self.connection_pools[db_name] = db_config
                elif db_type == 'oracle':
                    self.connection_pools[db_name] = db_config
                
                logger.info(f"Initialized connection pool for {db_name}")
            except Exception as e:
                logger.error(f"Failed to initialize pool for {db_name}: {str(e)}")
                raise
    
    def _create_postgres_pool(self, db_config: Dict, pool_size: int):
        """Create PostgreSQL connection pool."""
        return psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=pool_size,
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['username'],
            password=db_config['password'],
            sslmode=db_config.get('ssl_mode', 'prefer'),
            connect_timeout=db_config.get('connection_timeout', 30)
        )
    
    @contextmanager
    def get_connection(self, db_name: str = 'polyclinic_db'):
        """
        Context manager for database connections.
        
        Args:
            db_name: Name of the database configuration
            
        Yields:
            Database connection object
        """
        conn = None
        try:
            db_config = self.config['databases'][db_name]
            db_type = db_config.get('type', 'postgresql')
            
            if db_type == 'postgresql':
                conn = self.connection_pools[db_name].getconn()
            elif db_type == 'mysql':
                conn = self._create_mysql_connection(db_config)
            elif db_type in ['mssql', 'sqlserver']:
                conn = self._create_mssql_connection(db_config)
            elif db_type == 'oracle':
                conn = self._create_oracle_connection(db_config)
            
            # Set read-only if specified
            if db_config.get('read_only', False) and hasattr(conn, 'readonly'):
                conn.readonly = True
            
            yield conn
            
        except Exception as e:
            logger.error(f"Connection error for {db_name}: {str(e)}")
            raise
        finally:
            if conn:
                if db_type == 'postgresql' and db_name in self.connection_pools:
                    self.connection_pools[db_name].putconn(conn)
                else:
                    conn.close()
    
    def _create_mysql_connection(self, db_config: Dict):
        """Create MySQL connection."""
        return pymysql.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['username'],
            password=db_config['password'],
            connect_timeout=db_config.get('connection_timeout', 30),
            ssl={'ssl': db_config.get('ssl_mode') == 'require'}
        )
    
    def _create_mssql_connection(self, db_config: Dict):
        """Create MS SQL Server connection."""
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={db_config['host']},{db_config['port']};"
            f"DATABASE={db_config['database']};"
            f"UID={db_config['username']};"
            f"PWD={db_config['password']};"
        )
        if db_config.get('ssl_mode') == 'require':
            conn_str += "Encrypt=yes;TrustServerCertificate=no;"
        
        return pyodbc.connect(conn_str, timeout=db_config.get('connection_timeout', 30))
    
    def _create_oracle_connection(self, db_config: Dict):
        """Create Oracle connection."""
        dsn = cx_Oracle.makedsn(
            db_config['host'],
            db_config['port'],
            service_name=db_config['database']
        )
        return cx_Oracle.connect(
            user=db_config['username'],
            password=db_config['password'],
            dsn=dsn
        )
    
    def execute_query(
        self,
        query: str,
        params: Optional[Tuple] = None,
        db_name: str = 'polyclinic_db',
        fetch_size: Optional[int] = None
    ) -> List[Tuple]:
        """
        Execute a SQL query and return results.
        
        Args:
            query: SQL query to execute
            params: Query parameters
            db_name: Database name
            fetch_size: Number of rows to fetch at once
            
        Returns:
            List of result tuples
        """
        with self.get_connection(db_name) as conn:
            cursor = conn.cursor()
            
            try:
                # Set query timeout if configured
                query_timeout = self.config['extraction'].get('query_timeout', 300)
                if hasattr(cursor, 'execute_timeout'):
                    cursor.execute_timeout = query_timeout
                
                # Execute query
                cursor.execute(query, params or ())
                
                # Fetch results
                if fetch_size:
                    results = []
                    while True:
                        rows = cursor.fetchmany(fetch_size)
                        if not rows:
                            break
                        results.extend(rows)
                    return results
                else:
                    return cursor.fetchall()
                    
            except Exception as e:
                logger.error(f"Query execution error: {str(e)}")
                logger.debug(f"Query: {query}")
                raise
            finally:
                cursor.close()
    
    def execute_query_chunks(
        self,
        query: str,
        chunk_size: int = 10000,
        db_name: str = 'polyclinic_db'
    ):
        """
        Generator function to execute query and yield results in chunks.
        
        Args:
            query: SQL query to execute
            chunk_size: Number of rows per chunk
            db_name: Database name
            
        Yields:
            Chunks of result rows
        """
        with self.get_connection(db_name) as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute(query)
                
                while True:
                    rows = cursor.fetchmany(chunk_size)
                    if not rows:
                        break
                    yield rows
                    
            except Exception as e:
                logger.error(f"Query execution error: {str(e)}")
                raise
            finally:
                cursor.close()
    
    def get_column_names(self, cursor) -> List[str]:
        """Extract column names from cursor description."""
        if cursor.description:
            return [desc[0] for desc in cursor.description]
        return []
    
    def test_connection(self, db_name: str = 'polyclinic_db') -> bool:
        """
        Test database connection.
        
        Args:
            db_name: Database name
            
        Returns:
            True if connection successful, False otherwise
        """
        try:
            with self.get_connection(db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                cursor.close()
                logger.info(f"Connection test successful for {db_name}")
                return result[0] == 1
        except Exception as e:
            logger.error(f"Connection test failed for {db_name}: {str(e)}")
            return False
    
    def close_all_pools(self):
        """Close all connection pools."""
        for db_name, pool in self.connection_pools.items():
            if hasattr(pool, 'closeall'):
                pool.closeall()
                logger.info(f"Closed connection pool for {db_name}")
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        self.close_all_pools()

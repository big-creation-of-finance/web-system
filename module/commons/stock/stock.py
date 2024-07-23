import sqlite3
from pydantic import BaseModel


def create_table_from_dataclass(conn: sqlite3.Connection, dataclass_type: BaseModel):
    """根据dataclass定义的类型创建一张表
    Args:
        conn: SQLite3数据库连接
        dataclass_type: dataclass类型
    """
    table_name = dataclass_type.__name__
    columns = []
    for field_name, field_type in dataclass_type.__dataclass_fields__.items():
        sql_type = _get_sql_type(field_type.type)
        if sql_type is None:
            raise ValueError(f"不支持的类型: {field_type.type}")
        column_definition = f"{field_name} {sql_type}"
        if field_type.default_factory is not None:
            column_definition += " DEFAULT NULL"
        columns.append(column_definition)

    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {", ".join(columns)}
    );
    """
    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()


def _get_sql_type(python_type) -> str | None:
    """将Python类型映射到SQLite3数据类型"""
    type_mapping = {
        int: "INTEGER",
        str: "TEXT",
        float: "REAL",
        bool: "INTEGER",
    }
    return type_mapping.get(python_type)

from typing import List
from alembic.operations import Operations

def create_inherited_tables(op: Operations, base_table: str, child_tables: List[str]):
    """
    Create tables for inherited models in the correct order.
    
    Args:
        op: Alembic Operations object
        base_table: Name of the base table
        child_tables: List of child table names
    """
    # First create the base table
    op.create_table(base_table)
    
    # Then create child tables
    for child_table in child_tables:
        op.create_table(child_table)

def drop_inherited_tables(op: Operations, base_table: str, child_tables: List[str]):
    """
    Drop tables for inherited models in the correct order.
    
    Args:
        op: Alembic Operations object
        base_table: Name of the base table
        child_tables: List of child table names
    """
    # First drop child tables
    for child_table in child_tables:
        op.drop_table(child_table)
    
    # Then drop the base table
    op.drop_table(base_table)

def get_inheritance_dependencies(base_table: str, child_tables: List[str]) -> List[str]:
    """
    Get the correct order of table dependencies for inherited models.
    
    Args:
        base_table: Name of the base table
        child_tables: List of child table names
    
    Returns:
        List of table names in the correct order for creation/deletion
    """
    return [base_table] + child_tables 
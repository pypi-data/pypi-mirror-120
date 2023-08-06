
__all__ = ['parse']

from typing import List
from sqlalchemy.ext.automap import AutomapBase
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import Table, Column
import yaml
from yamlalchemy.contants import *
from sqlalchemy import MetaData
from sqlalchemy.sql.functions import func
from yamlalchemy.statement import _order, _where, _limit, _offset, _having


metadata = MetaData()


class QueryBuilder:
    session = None
    table = None
    columns = []
    group = []
    order_by = []
    where = []
    having = []
    limit = None
    offset = None

    def __init__(self, session: Session):
        self.session = session

    def set_table(self, table: Table):
        self.table = table

    def set_columns(self, columns: List[Column]):
        self.columns = columns

    def set_group(self, group: List[Column]):
        self.group = group

    def set_order_by(self, order_by: List[Column]):
        self.order_by = order_by

    def set_where(self, where_clause: List[Column]):
        self.where = where_clause

    def set_having(self, having_clause: List[Column]):
        self.having = having_clause

    def set_limit(self, limit: int):
        self.limit = limit

    def set_offset(self, offset: int):
        self.offset = offset

    def to_query(self):
        query = self.session.query(self.table)
        query = query.with_entities(*self.columns)
        query = query.filter(*self.where)
        query = query.group_by(*self.group)
        query = query.order_by(*self.order_by)
        query = _having(self.having, query)
        query = _limit(self.limit, query)
        query = _offset(self.offset, query)

        return query


def query_fragment(table: Table, columns: List[dict]) -> List[Column]:
    """
    args:
        table: SQLAlchemy table class
        columns: yaml table dictionary.
    """

    if isinstance(columns, list) is False:
        raise Exception(
            f"Columns must be list. {type(columns)} given.")

    cols = []
    for column in columns:
        name = column.get(NAME, None)
        alias = column.get(ALIAS, None)
        expr = column.get(FUNC, None)
        direction = column.get(DIRECTION, None)
        where_clause = column.get(FILTER, None)
        col = getattr(table, name)

        if expr is not None:
            column_aggr_func = getattr(func, expr)
            col = column_aggr_func(col)
            col = col.label(name)

        if direction is not None and direction in QUERY_ORDERS:
            col = _order(col, direction)

        if where_clause is not None:
            col = _where(col, where_clause)

        if alias:
            col = col.label(alias)

        cols.append(col)

    return cols


def parse(yaml_content: str or dict, session: Session, reflection: AutomapBase) -> "QueryBuilder":
    """
    Initial entry point for yamlalchemy.
    Parses the given YAML string to create a SqlAlchemy query

    args:
        yaml_content: YAML content or Python dictionary.
        session: SqlAlchemy Session
        reflection: SqlAlchemy AutomapBase
    """

    if not yaml_content:
        raise Exception('No yaml content given.')
    qd = yaml_content

    if isinstance(yaml_content, dict) is False:
        qd = yaml.safe_load(yaml_content)

    if not isinstance(qd, dict):
        raise TypeError(
            "Argument for query parsing must be a Python dictionary.")

    if FROM not in qd:
        raise Exception(f"Missing \"{FROM}\" argument in query.")

    if COLUMN not in qd:
        qd[COLUMN] = []

    if GROUP not in qd:
        qd[GROUP] = []

    if ORDER not in qd:
        qd[ORDER] = []

    if WHERE not in qd:
        qd[WHERE] = []

    if HAVING not in qd:
        qd[HAVING] = []

    if LIMIT not in qd:
        qd[LIMIT] = None

    if OFFSET not in qd:
        qd[OFFSET] = None

    table = reflection.classes[qd[FROM]]
    columns = query_fragment(table, qd[COLUMN])
    group_by = query_fragment(table, qd[GROUP])
    order_by = query_fragment(table, qd[ORDER])
    where = query_fragment(table, qd[WHERE])
    having = query_fragment(table, qd[HAVING])

    limit = qd[LIMIT]
    offset = qd[OFFSET]

    qb = QueryBuilder(session=session)
    qb.set_table(table)
    qb.set_columns(columns)
    qb.set_where(where)
    qb.set_group(group_by)
    qb.set_having(having)
    qb.set_order_by(order_by)
    qb.set_limit(limit)
    qb.set_offset(offset)

    return qb

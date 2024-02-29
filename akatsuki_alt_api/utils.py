from typing import Any, List, Self, Tuple

EQUALS = "{K}=={V}"
LESS_THAN = "{K}<{V}"
GREATER_THAN = "{K}>{V}"


class Query:
    
    def __init__(self, default_queries: str = ""):
        self.query = default_queries
    
    def _add_to_query(self, fmt_str: str):
        if self.query:
            self.query += f",{fmt_str}"
        else:
            self.query = fmt_str

    def equals(self, key: str, value: Any) -> Self:
        self._add_to_query(EQUALS.format(K=key, V=value))
        return self

    def less_than(self, key: str, value: Any) -> Self:
        self._add_to_query(LESS_THAN.format(K=key, V=value))
        return self

    def greater_than(self, key: str, value: Any) -> Self:
        self._add_to_query(GREATER_THAN.format(K=key, V=value))
        return self

    def execute(self):
        pass

class PaginatedQuery(Query):
    
    def __init__(self, default_queries: str = ""):
        self._page = 0
        super().__init__(default_queries)
    
    def execute(self) -> Any:
        pass
    
    def prev(self):
        self._page = max(1, self._page - 1)
        return self.execute()
    
    def next(self):
        self._page += 1
        return self.execute()

# server/backend_app/parser/query_process.py

from .operation.query_manipulate import Query_manipulate
from .Function.Show_db import show_db
from .operation.Simple_Generate import simple_generate
from .operation.Generate import generate
from .operation.Inspect import inspect
from .operation.Construct import construct
from .operation.Drop_dataset import drop_dataset
from .operation.Temp_Generate import temp_generate
from .operation.Clustering import clustering_generate
from .Function.Imputer import impute

def query_process(query,user=None):
    """
    Dispatches the user query to the appropriate handler.
    Yields:
        dict: response from the handler
    """
    query_upper = query.strip().upper()

    if query_upper.startswith("GENERATE") and "CLUSTERING" in query_upper:
        yield clustering_generate(query, user)
        return

    dispatch_map = [
        ("SHOW", show_db),
        ("CONSTRUCT", construct),
        ("GENERATE", lambda q: generate(q,user) if " BEST ALGORITHM " in q.upper() else temp_generate(q,user)),
        ("INSPECT", inspect),
        # ("IMPUTE", impute),
        ("DROP", drop_dataset),
    ]

    for prefix, handler in dispatch_map:
        if query_upper.startswith(prefix):
            yield handler(query)
            return

    # Default: treat as SQL or custom query
    yield Query_manipulate(query)
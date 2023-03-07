from typing import Any
import numpy as np
from psycopg2.extensions import register_adapter, AsIs


def adapt_numpy_float64(inp: np.float64) -> AsIs:
    return AsIs(inp)


def adapt_numpy_int64(inp: np.int64) -> AsIs:
    return AsIs(inp)


def adapt_numpy_float32(inp: np.float32) -> AsIs:
    return AsIs(inp)


def adapt_numpy_int32(inp: np.int32) -> AsIs:
    return AsIs(inp)


def adapt_numpy_array(inp: np.ndarray[Any]) -> AsIs:
    return AsIs(tuple(inp))


register_adapter(np.float64, adapt_numpy_float64)
register_adapter(np.int64, adapt_numpy_int64)
register_adapter(np.float32, adapt_numpy_float32)
register_adapter(np.int32, adapt_numpy_int32)
register_adapter(np.ndarray, adapt_numpy_array)

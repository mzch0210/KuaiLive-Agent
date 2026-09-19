from __future__ import annotations

import ast
import numpy as np

import fair_residual_validation as base


def parse_list(text: str, dtype=float) -> np.ndarray:
    """Parse ReChorus CSV list cells emitted from NumPy scalar objects.

    NumPy 1.26 may serialize object-list cells as e.g.
    [np.float32(0.1), np.float32(-0.2)] or [np.int64(3), np.int64(4)].
    Strip the scalar constructors before literal evaluation.
    """
    s = str(text).strip()
    for token in (
        "np.float16(", "np.float32(", "np.float64(",
        "np.int8(", "np.int16(", "np.int32(", "np.int64(",
        "np.uint8(", "np.uint16(", "np.uint32(", "np.uint64(",
    ):
        s = s.replace(token, "")
    s = s.replace(")", "")
    return np.asarray(ast.literal_eval(s), dtype=dtype)


base.parse_list = parse_list


if __name__ == "__main__":
    # Fail fast on the exact serialization forms expected from ReChorus/pandas.
    assert parse_list("[np.int64(3), np.int64(4)]", int).tolist() == [3, 4]
    assert np.allclose(parse_list("[np.float32(0.1), np.float64(-0.2)]", float), [0.1, -0.2])
    base.main()

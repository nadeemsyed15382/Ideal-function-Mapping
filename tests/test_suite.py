import pandas as pd
from src.function_selector import FunctionSelector

def test_least_squares_basic():
    train = pd.DataFrame({"x":[0,1,2], "y1":[0,1,2], "y2":[2,3,4], "y3":[1,1,1], "y4":[0,0,0]})
    ideal = pd.DataFrame({"x":[0,1,2], "i1":[0,1,2], "i2":[0,2,4], "i3":[1,1,1], "i4":[5,5,5]})
    sel = FunctionSelector(train, ideal).select()
    assert len(sel) == 4
    # y1 should match i1, y3 -> i3 likely, etc.
    assert sel["y1"]["ideal_col"] == "i1"

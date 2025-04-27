from __future__ import annotations

from hypothesis import given
from hypothesis.strategies import DrawFn, booleans, composite, lists, tuples
from polars import Int64, String
from utilities.hypothesis import int64s, text_ascii

from polars_subclasses.lib import DataFrameWithMetaData


class DataFrameWithBool(DataFrameWithMetaData[bool]): ...


@composite
def dataframes_with_bool(draw: DrawFn, /) -> DataFrameWithBool:
    rows = draw(lists(tuples(int64s(), text_ascii())))
    bool_ = draw(booleans())
    return DataFrameWithBool(
        data=rows, schema={"x": Int64, "y": String}, orient="row", metadata=bool_
    )


class TestDataFrameWithMeta:
    @given(df=dataframes_with_bool())
    def test_main(self, *, df: DataFrameWithBool) -> None:
        assert isinstance(df, DataFrameWithMetaData)

    @given(df=dataframes_with_bool())
    def test_with_columns(self, *, df: DataFrameWithBool) -> None:
        result = df.with_columns()
        assert isinstance(result, DataFrameWithMetaData)
        assert result.metadata is df.metadata

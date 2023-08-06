from dataclasses import dataclass
from typing import List
from typing import Optional

from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import StrictUndefined

from tecton_proto.data.feature_service_pb2 import FeatureSetItem
from tecton_proto.data.feature_view_pb2 import NewTemporalAggregate
from tecton_spark.aggregation_utils import get_aggregation_function_name
from tecton_spark.snowflake_pipeline_helper import pipeline_to_sql_string

TEMPLATE = None


def snowflake_function(value):
    fn = get_aggregation_function_name(value)
    if fn == "mean":
        return "avg"
    return fn


def _load_template():
    # TODO: Do this at module loading time once we sort out including the templates in the public SDK build
    global TEMPLATE
    if TEMPLATE:
        return
    env = Environment(
        loader=PackageLoader("tecton_spark"),
        autoescape=False,
        undefined=StrictUndefined,
    )
    env.filters["snowflake_function"] = snowflake_function
    TEMPLATE = env.get_template("historical_features.sql")


@dataclass
class _FeatureSetItemInput:
    """A simplified version of FeatureSetItem which is passed to the SQL template."""

    name: str
    timestamp_key: str
    join_keys: List[str]
    features: List[str]
    sql: str
    aggregation: Optional[NewTemporalAggregate]


# TODO: We need to figure out a better way to format our SQL string
def get_features_sql_str_for_spine(
    feature_set_items: List[FeatureSetItem],
    timestamp_key: str,
    spine_sql: Optional[str] = None,
    include_feature_package_timestamp_columns: bool = False,
) -> str:
    """
    Get a SQL string to fetch features given the spine and feature set.
    spine_sql and spine_table_name cannot be both empty.

    :param feature_set_items: FeatureSetItems for the features.
    :param timestamp_key: Name of the time column in the spine.
    :param spine_sql: SQL str to get the spine.
    :param include_feature_package_timestamp_columns: (Optional) Include timestamp columns for every individual FeaturePackage.
    :return: A SQL string that can be used to fetch features.
    """
    _load_template()
    if include_feature_package_timestamp_columns:
        raise NotImplementedError()

    input_items = []
    for item in feature_set_items:
        feature_view = item.enrichments.feature_view
        if len(feature_view.online_serving_index.join_keys) != len(feature_view.join_keys):
            raise ValueError("SQL string does not support wildcard")
        input_items.append(
            _FeatureSetItemInput(
                name=feature_view.fco_metadata.name,
                timestamp_key=feature_view.timestamp_key,
                join_keys={k.package_column_name: k.spine_column_name for k in item.join_configuration_items},
                features=item.feature_columns,
                sql=pipeline_to_sql_string(
                    pipeline=feature_view.pipeline,
                    virtual_data_sources=feature_view.enrichments.virtual_data_sources,
                    transformations=feature_view.enrichments.transformations,
                ),
                aggregation=(
                    feature_view.temporal_aggregate
                    if item.enrichments.feature_view.HasField("temporal_aggregate")
                    else None
                ),
            )
        )
    return TEMPLATE.render(
        feature_set_items=input_items,
        spine_timestamp_key=timestamp_key,
        spine_sql=spine_sql,
        include_feature_package_timestamp_columns=include_feature_package_timestamp_columns,
    )

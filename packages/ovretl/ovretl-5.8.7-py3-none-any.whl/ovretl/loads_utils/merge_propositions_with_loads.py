import pandas as pd


def merge_with_propositions_loads(
    propositions_df: pd.DataFrame, propositions_loads_df: pd.DataFrame) -> pd.DataFrame:
    propositions_df = pd.merge(
        propositions_df,
        propositions_loads_df[
            [
                "total_number",
                "total_volume",
                "total_weight",
                "taxable_weight",
                "weight_measurable",
                "hazardous",
                "lithium",
                "non_stackable",
                "proposition_id",
            ]
        ],
        how="left",
        on="proposition_id",
    ).reset_index(drop=True).rename(columns={"hazardous": "loads_hazardous", "magnetic": "loads_magnetic",
                                             "lithium": "loads_lithium", "refrigerated": "loads_refrigerated"})
    return propositions_df


def merge_propositions_with_loads(
        propositions_df: pd.DataFrame, propositions_loads_df: pd.DataFrame, drop_duplicate_key="proposition_id"
):
    propositions_df = merge_with_propositions_loads(
        propositions_df=propositions_df, propositions_loads_df=propositions_loads_df
    )
    propositions_df = propositions_df.sort_values(by=["total_weight", "total_volume"], ascending=False)
    propositions_df = propositions_df[
        (~propositions_df.duplicated(subset=[drop_duplicate_key])) | (propositions_df[drop_duplicate_key].isnull())
    ]  # drop duplicates without dropping nan
    return propositions_df

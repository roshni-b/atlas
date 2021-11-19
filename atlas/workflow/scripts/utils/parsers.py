import pandas as pd


def read_checkm_output(taxonomy_table, completness_table):

    c_df = pd.read_csv(completness_table, index_col=0, sep="\t")[
        ["Completeness", "Contamination", "Strain heterogeneity"]
    ]
    t_df = pd.read_csv(taxonomy_table, index_col=0, sep="\t")[
        [
            "# unique markers (of 43)",
            "# multi-copy",
            "Insertion branch UID",
            "Taxonomy (contained)",
            "Taxonomy (sister lineage)",
            "GC",
            "Genome size (Mbp)",
            "Gene count",
            "Coding density",
        ]
    ]
    df = pd.concat([c_df, t_df], axis=1)
    return df

def read_busco_output(completness_table,
                      quality_score_formula="Completeness - 5*Contamination - (fragmented_busco/total_busco)"
                      ):


    df= pd.read_table(completness_table,index_col=0)

    df.eval(
            "Completeness = (complete_busco + 0.5 * fragmented_busco) / total_busco",
            inplace=True,
        )
    df.eval(
            "Contamination = duplicated_busco / total_busco", inplace=True
        )
    df.eval(
            "Quality_score = "+quality_score_formula,
            inplace=True,
        )

    return df

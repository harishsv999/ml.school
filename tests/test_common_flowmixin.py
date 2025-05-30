from pathlib import Path

import pandas as pd
import pytest
from metaflow import Run, Runner


@pytest.fixture(scope="module")
def metaflow_data():
    with Runner("tests/flowmixin_flow.py", show_output=False).run() as running:
        return Run(running.run.pathspec).data


def test_load_dataset(metaflow_data):
    penguins = pd.read_csv(Path("data/penguins.csv"))
    assert len(metaflow_data.data) == len(penguins)


def test_load_dataset_cleans_sex_column(metaflow_data):
    sex_distribution = metaflow_data.data["sex"].value_counts()

    assert len(sex_distribution) == len(["MAKE", "FEMALE"])
    assert sex_distribution.index[0] == "MALE"
    assert sex_distribution.index[1] == "FEMALE"

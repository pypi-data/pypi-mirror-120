import typing as t

import numpy as np
import pandas as pd

from deploy_chk import __version__ as _version
from deploy_chk.config.core import config
from deploy_chk.processing.data_manager import load_pipeline, load_dataset
from deploy_chk.processing.validation import validate_inputs

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
_sales_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction(
    *,
    input_data: t.Union[pd.DataFrame, dict],
) -> dict:
    """Make a prediction using a saved model pipeline."""

    data = pd.DataFrame(input_data)
    validated_data, errors = validate_inputs(input_data=data)
    results = {"predictions": None, "version": _version, "errors": errors}

    if not errors:
        predictions = _sales_pipe.predict(
            X=validated_data[config.model_config.features]
        )
        results = {
            "predictions": predictions,  # type: ignore
            "version": _version,
            "errors": errors,
        }

    return results


from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from deploy_chk.config.core import config


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""

    #input_data["StateHoliday"] = input_data["StateHoliday"].astype("str")
    #input_data = input_data.drop("Customers", axis = 1)

    validated_data = input_data[config.model_config.features].copy()
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleHouseDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class HouseDataInputSchema(BaseModel):
    Store: Optional[int]
    DayOfWeek: Optional[int]
    Date: Optional[str]
    Open: Optional[int]
    Promo: Optional[int]
    StateHoliday: Optional[str]
    SchoolHoliday: Optional[int]
    StoreType: Optional[str]
    Assortment: Optional[str]
    CompetitionDistance: Optional[int]
    CompetitionOpenSinceMonth: Optional[int]
    CompetitionOpenSinceYear: Optional[int]
    Promo2: Optional[int]
    Promo2SinceWeek: Optional[int]
    Promo2SinceYear: Optional[int]
    PromoInterval: Optional[str]


class MultipleHouseDataInputs(BaseModel):
    inputs: List[HouseDataInputSchema]

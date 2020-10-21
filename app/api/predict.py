import logging
import random

from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator

log = logging.getLogger(__name__)
router = APIRouter()


class BnB(BaseModel):
    """Use this data model to parse the request body JSON."""
    accomodates: int
    bathrooms: float
    bedrooms: int
    beds: int
    guests_included: int
    min_nights: int
    max_nights: int

    def to_df(self):
        """Convert pydantic object to pandas dataframe with 1 row."""
        return pd.DataFrame([dict(self)])

@router.post('/predict')
async def predict(bnb: BnB):
    """
    Make predictions of air bnb optimal prices

    ### Request Body
    - accomodates: int
    - bathrooms: float
    - bedrooms: int
    - beds: int
    - guests_included: int
    - min_nights: int
    - max_nights: int

    ### Response
    - `prediction`: optimal price for air bnb with these characteristics
    representing the predicted class's probability

    Replace the placeholder docstring and fake predictions with your own model.
    """
    X_new = bnb.to_df()
    log.info(X_new)
    acc = X_new['accomodates']
    baths = X_new['bathrooms']
    bedrooms = X_new['bedrooms']
    beds = X_new['beds']
    guests = X_new['guests_included']
    min_n = X_new['min_nights']
    max_n = X_new['max_nights']
    
    #optimal_price = new_model.predict(X_new)
    y_pred = (acc*10) + (baths*10) + (bedrooms*10) + (beds*10) + (guests*10)
    
    return {'predicted_price': y_pred}

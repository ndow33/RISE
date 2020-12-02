from fastapi import APIRouter, HTTPException
import pandas as pd
import plotly.express as px
from app.api.rise_class import Rise

router = APIRouter()


@router.post('/rise/{name}')
async def rise(name: str):
    """
    Valid inputs: 
    steinaker,
    redfleet,
    flaming 
    **********************

    Returns data from the Bureau of Reclamation's [RISE catalog](https://data.usbr.gov/catalog).

    [Link](https://data.usbr.gov/rise/api/) to RISE api documentation
    """

    # create a rise object
    rise = Rise(name)

    # validate the name
    name = name.lower()
    if name not in rise.bodies:
        raise HTTPException(status_code=404, detail=f'Name {name} not found')

    # return our object
    return rise.results

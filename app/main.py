from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api import rise

app = FastAPI(
    title='WETx API',
    description='Connects to different water data APIs and aggregates the data into an easy to use format',
    version='0.1',
    docs_url='/',
)
# add routes here

app.include_router(rise.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)

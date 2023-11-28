import uvicorn

from .fastserve import app

uvicorn.run(app)

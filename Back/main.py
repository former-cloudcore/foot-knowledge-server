from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pathlib
import uvicorn

from routers import (
    leagues,
    players,
    player_team,
    teams,
    games,
    scoreboard,
    specials
)
from const import (
    OPEN_API_DESCRIPTION,
    OPEN_API_TITLE,
)
from middleware.auth_middleware import AuthMiddleware  # Import the middleware

templates = Jinja2Templates(directory="templates")

app = FastAPI(
    title=OPEN_API_TITLE,
    description=OPEN_API_DESCRIPTION,
    version='0.4',
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthMiddleware)  # Add the authentication middleware

app.mount("/assets", StaticFiles(directory=pathlib.Path(__file__).parent / 'static'), name="static")

@app.get("/favicon.ico")
async def get_favicon():
    return FileResponse("static/favicon.ico")

app.include_router(leagues.router)
app.include_router(players.router)
app.include_router(player_team.router)
app.include_router(teams.router)
app.include_router(games.router)
app.include_router(scoreboard.router)
app.include_router(specials.router)
app.include_router(games.router)

@app.get("/{full_path:path}")
async def catch_all(request, full_path: str):
    print("full_path: "+full_path)
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=3000, reload=True, workers=1)

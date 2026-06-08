from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title="GamePy",
    description="A simple API to track retro games I want to play",
    version="0.1alpha"
)


game_db = [
    {"id": 1, "title": "Ultima I: The First Age of Darkness",
        "year": 1981, "is_completed": True},
    {"id": 2, "title": "Might and Magic II: Gates to Another World",
        "year": 1988, "is_completed": False}
]


class GameCreate(BaseModel):
    title: str
    year: int
    is_completed: bool = False


class GameResponse(BaseModel):
    id: int
    title: str
    year: int
    is_completed: bool = False


@app.post("/games", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
def add_game(game: GameCreate):
    new_id = game_db[-1]["id"] + 1 if game_db else 1
    new_game = {
        "id": new_id,
        "title": game.title,
        "year": game.year,
        "is_completed": game.is_completed
    }
    game_db.append(new_game)
    return new_game


@app.get("/games", response_model=list[GameResponse])
def get_all_games():
    return game_db


@app.get("/games/{game_id}", response_model=GameResponse)
def get_game(game_id: int):
    for game in game_db:
        if game["id"] == game_id:
            return game
    raise HTTPException(status_code=404, detail="Game was not found")


@app.put("/games/{game_id}", response_model=GameResponse)
def update_game(game_id: int, updated_data: GameCreate):
    for game in game_db:
        if game["id"] == game_id:
            game["title"] = updated_data.title
            game["year"] = updated_data.year
            game["is_completed"] = updated_data.is_completed
            return game
    raise HTTPException(status_code=404, detail="Game was not found")


@app.delete("/games/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game(game_id: int):
    for index, game in enumerate(game_db):
        if game["id"] == game_id:
            game_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="Game was not found")

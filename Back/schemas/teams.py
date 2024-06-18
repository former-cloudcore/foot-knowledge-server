from pydantic import BaseModel


class TeamSchema(BaseModel):
    name: str
    league_id: str
    ref: str
    team_id: str
    img_ref: str


class ConnectionSchema(BaseModel):
    team_name: str
    years: str
from typing import List,Optional

from sqlalchemy import select
from unidecode import unidecode


from models.players import PlayerModel
from schemas.players import PlayerSchema, PlayersSlimSchema
from services.base import (
    BaseDataManager,
    BaseService,
)


class PlayerService(BaseService):
    async def get_player(self, player_id: int) -> PlayersSlimSchema:
        """Get player by ID."""

        return await PlayerDataManager(self.session).get_player(player_id)

    async def get_players(self) -> List[PlayersSlimSchema]:
        """Select all players"""

        return await PlayerDataManager(self.session).get_players()

    async def search_players(self, name: str, nationality: str) -> List[PlayersSlimSchema]:
        """Search players by name"""
        return await PlayerDataManager(self.session).search_players(name=name, nationality=nationality)

    async def get_nationalities(self) -> List[str]:
        return await PlayerDataManager(self.session).get_nationalities()


class PlayerDataManager(BaseDataManager):
    async def get_player(self, player_id: int) -> PlayersSlimSchema:
        stmt = select(PlayerModel).where(PlayerModel.player_id == player_id)
        model = await self.get_one(stmt)

        return PlayersSlimSchema(**model.to_dict())

    async def get_players(self) -> List[PlayersSlimSchema]:
        schemas: List[PlayersSlimSchema] = list()

        stmt = select(PlayerModel).limit(100)

        for model in await self.get_all(stmt):
            schemas += [PlayersSlimSchema(**model.to_dict())]

        return schemas

    async def search_players(self, name: str, nationality: str) -> List[PlayersSlimSchema]:
        schemas: List[PlayersSlimSchema] = list()
        stmt = select(PlayerModel).where(PlayerModel.name_unaccented.like('%' + unidecode(name) + '%')).where(PlayerModel.nationality.like('%'+nationality+'%')).limit(100)
        for model in await self.get_all(stmt):
            schemas += [PlayersSlimSchema(**model.to_dict())]
        return schemas

    async def get_nationalities(self) -> list[str]:
        stmt = select(PlayerModel.nationality).group_by(PlayerModel.nationality)
        result = await self.get_all(stmt)
        result.remove(None)
        return result

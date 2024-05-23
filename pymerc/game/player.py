from __future__ import annotations

from typing import TYPE_CHECKING

from pymerc.api.models import common
from pymerc.api.models.player import Household, Sustenance
from pymerc.api.models.player import Player as PlayerModel
from pymerc.game.building import BuildingsList
from pymerc.game.exports import ExportsList, ExportsSummed
from pymerc.game.imports import ImportsList, ImportsSummed
from pymerc.game.transport import Transport

if TYPE_CHECKING:
    from pymerc.client import Client


class Player:
    """A higher level representation of a player in the game."""

    buildings: BuildingsList
    business: common.Business
    data: PlayerModel
    exports: ExportsSummed
    imports: ImportsSummed
    transports: list[Transport]

    def __init__(self, client: Client):
        self._client = client
        self.buildings = BuildingsList()
        self.exports = ExportsSummed()
        self.imports = ImportsSummed()

    async def load(self):
        """Loads the data for the player."""
        self.data = await self._client.player_api.get()
        self.business = await self._client.businesses_api.get(
            self.data.household.business_ids[0]
        )

        for id in self.business.building_ids:
            self.buildings.append(await self._client.building(id))

        self.transports = []
        for id in self.business.transport_ids:
            self.transports.append(await self._client.transport(id))

        for transport in self.transports:
            for item, exp in transport.exports.items():
                if item not in self.exports:
                    self.exports[item] = ExportsList([exp])
                else:
                    self.exports[item].append(exp)

            for item, imp in transport.imports.items():
                if item not in self.imports:
                    self.imports[item] = ImportsList([imp])
                else:
                    self.imports[item].append(imp)

        self.storehouse = await self._client.storehouse(self)

    @property
    def household(self) -> Household:
        """The household of the player."""
        return self.data.household

    @property
    def money(self) -> float:
        """The amount of money the player has."""
        return self.business.account.assets.get(common.Asset.Money).balance

    @property
    def prestige(self) -> float:
        """The prestige of the player."""
        return self.data.household.prestige

    @property
    def sustenance(self) -> Sustenance:
        """The sustenance of the player."""
        return self.data.household.sustenance

    @property
    def sustenance_cost(self) -> float:
        """The cost of the player's sustenance."""
        total_cost = 0
        for item in self.sustenance_items:
            total_cost += self.sustenance_item_cost(item)

        return total_cost

    @property
    def sustenance_items(self) -> list[common.Item]:
        """The items currently being consumed by the player's sustenance."""
        return self.data.household.sustenance.inventory.managers.keys()

    def sustenance_item_consumption(self, item: common.Item) -> float:
        """The amount of an item consumed by the player's sustenance."""
        return self.data.household.sustenance.inventory.previous_flows[item].consumption

    def sustenance_item_cost(self, item: common.Item) -> float:
        """The cost of an item consumed by the player's sustenance."""
        return (
            self.sustenance_item_consumption(item)
            * self.storehouse.items[item].average_cost
        )

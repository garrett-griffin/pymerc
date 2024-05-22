from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pymerc.api.models.buildings import Building
from pymerc.api.models import common

if TYPE_CHECKING:
    from pymerc.client import Client


class Player:
    """A higher level representation of a player in the game."""

    def __init__(self, client: Client):
        self._client = client

    async def load(self):
        """Loads the data for the player."""
        self.data = await self._client.player_api.get()
        self.business = await self._client.businesses_api.get(self.data.household.business_ids[0])

        self.transports = []
        for id in self.business.transport_ids:
            self.transports.append(await self._client.transport(id))

        self.storehouse = await self._client.building(self._get_storehouse_id())

    @property
    def buildings(self) -> list[Building]:
        """The buildings the player owns."""
        return self.business.buildings

    @property
    def money(self) -> float:
        """The amount of money the player has."""
        return self.business.account.assets.get(common.Asset.Money).balance

    def item(self, item: common.Item) -> Optional[common.InventoryAccountAsset]:
        """Get an item from the player's storehouse.

        Args:
            item (Item): The item to get.

        Returns:
            Optional[InventoryAccountAsset]: The item, if it exists.
        """
        return self.storehouse.items.get(item, None)

    def previous_item_flow(self, item: common.Item) -> Optional[common.InventoryFlow]:
        """Get the previous flow of an item from the player's storehouse.

        Args:
            item (Item): The item to get.

        Returns:
            Optional[InventoryFlow]: The flow of the item, if it exists.
        """
        return self.storehouse.previous_flows.get(item, None)

    def item_flow(self, item: common.Item) -> Optional[common.InventoryFlow]:
        """Get the flow of an item from the player's storehouse.

        Args:
            item (Item): The item to get.

        Returns:
            Optional[InventoryFlow]: The flow of the item, if it exists.
        """
        return self.storehouse.flows.get(item, None)

    def _get_storehouse_id(self) -> Optional[int]:
        """Get the ID of the player's storehouse.

        Returns:
            Optional[int]: The ID of the storehouse, if it exists.
        """
        storehouses = [
            building.id
            for building in self.business.buildings
            if building.type == common.BuildingType.Storehouse
        ]

        if storehouses:
            return storehouses[0]
        else:
            return None
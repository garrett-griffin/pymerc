from __future__ import annotations

from collections import UserList
from typing import TYPE_CHECKING, Optional

from pymerc.api.models import common
from pymerc.api.models.buildings import Building as BuildingModel
from pymerc.game.recipe import Recipe

if TYPE_CHECKING:
    from pymerc.client import Client


class Building:
    """A higher level representation of a building in the game."""

    data: BuildingModel

    def __init__(self, client: Client, id: int):
        self._client = client
        self.id = id

    async def load(self):
        """Loads the data for the building."""
        self.data = await self._client.buildings_api.get(self.id)
        self.operations_data = await self._client.buildings_api.get_operations(self.id)

    @property
    def flows(self) -> Optional[dict[common.Item, common.InventoryFlow]]:
        """The flows of the building."""
        return self.operations_data.total_flow

    @property
    def inventory(self) -> Optional[common.Inventory]:
        """Returns the inventory of the building."""
        if self.data and self.data.storage:
            return self.data.storage.inventory
        return None

    @property
    def items(self) -> Optional[dict[common.Item, common.InventoryAccountAsset]]:
        """Returns the items in the building's storage."""
        if self.data and self.data.storage:
            return self.data.storage.inventory.account.assets
        else:
            return None

    @property
    def managers(self) -> dict[common.Item, common.InventoryManager]:
        """The managers of the building."""
        return self.data.storage.inventory.managers

    @property
    def operations(self) -> Optional[list[common.Operation]]:
        """The operations of the building."""
        return self.operations_data.operations

    @property
    def previous_flows(self) -> Optional[dict[common.Item, common.InventoryFlow]]:
        """The flows of the building."""
        if self.data.storage:
            return self.data.storage.inventory.previous_flows
        else:
            return None

    @property
    def production(self) -> Optional[common.Producer]:
        """Returns the production of the building."""
        return self.data.producer if self.data else None

    @property
    def production_flows(self) -> Optional[dict[common.Item, common.InventoryFlow]]:
        """Returns the production flows of the building."""
        if self.data and self.data.producer:
            return self.data.producer.inventory.previous_flows
        else:
            return None

    @property
    def size(self) -> Optional[int]:
        """Returns the size of the building."""
        return self.data.size if self.data else None

    @property
    def target_production(self) -> Optional[float]:
        """Returns the production target of the building."""
        return (
            self.production.target
            if self.production and self.production.target
            else 0.0
        )

    @property
    def type(self) -> common.BuildingType:
        """Returns the type of the building."""
        return self.data.type if self.data else None

    @property
    def under_construction(self) -> bool:
        """Returns whether the building is under construction."""
        return self.data.construction is not None if self.data else False

    @property
    def upgrades(self) -> Optional[list[common.BuildingUpgradeType]]:
        """Returns the upgrades installed for the building."""
        return self.data.upgrades if self.data else None

    def flow(self, item: common.Item) -> Optional[common.InventoryFlow]:
        """Get the flow of an item in the building.

        Args:
            item (Item): The item.

        Returns:
            Optional[InventoryFlow]: The flow of the item, if it exists.
        """
        if self.data.storage:
            return self.data.storage.inventory.previous_flows.get(item, None)
        else:
            return None

    def item(self, item: common.Item) -> Optional[common.InventoryAccountAsset]:
        """Get an item in the building.

        Args:
            item (Item): The item.

        Returns:
            Optional[InventoryAccountAsset]: The item, if it exists.
        """
        if self.data.storage:
            return self.data.storage.inventory.account.assets.get(item, None)
        else:
            return None

    def manager(self, item: common.Item) -> Optional[common.InventoryManager]:
        """Get the manager of an item in the building.

        Args:
            item (Item): The item.

        Returns:
            Optional[InventoryManager]: The manager of the item, if it exists.
        """
        if self.data.storage:
            return self.data.storage.inventory.managers.get(item, None)
        else:
            return None

    def set_manager(self, item: common.Item, manager: common.InventoryManager) -> bool:
        """Set the manager for an item in the building.

        Args:
            item (Item): The item.
            manager (InventoryManager): The manager.

        Returns:
            bool: Whether the manager was set.
        """
        return self._client.buildings_api.set_manager(self.id, item, manager)

    async def calculate_current_labor_need(self) -> float:
        """Calculates the current labor need based on the building's production recipe.
        Returns:
            float: The labor required for the target multiplier.
        """
        if self.production:
            recipe = Recipe(self._client, self.production.recipe.value)
            await recipe.load()
            if recipe:
                if self.items:
                    inventory_assets = self.items
                elif self.data and self.data.producer:
                    inventory_assets = self.data.producer.inventory.account.assets
                else:
                    inventory_assets = []
                if self.data and self.data.storage:
                    inventory_managers = self.data.storage.inventory.managers
                elif self.data and self.data.producer:
                    inventory_managers = self.data.producer.inventory.managers
                else:
                    inventory_managers = []

                return recipe.calculate_target_labor(
                    self.target_production, inventory_assets, inventory_managers
                )

        return 0.0


class BuildingsList(UserList):
    """A list of buildings."""

    def by_type(self, type: common.BuildingType) -> BuildingsList:
        """Get all buildings of a certain type.

        Args:
            type (BuildingType): The type of the buildings.

        Returns:
            BuildingsList: The buildings of the given type.
        """
        return BuildingsList([b for b in self if b.type == type])

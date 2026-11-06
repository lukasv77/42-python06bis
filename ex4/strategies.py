from ex3.capability import TransformCapability
from ex3.creature import Creature

from .errors import InvalidStrategyError
from .strategy import BattleStrategy


class NormalStrategy(BattleStrategy):
    def __init__(self) -> None:
        super().__init__("Normal")

    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> None:
        print(creature.attack())


class AggressiveStrategy(BattleStrategy):
    def __init__(self) -> None:
        super().__init__("Aggressive")

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> None:
        if not isinstance(creature, TransformCapability):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}' "
                "for this aggressive strategy"
            )
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())

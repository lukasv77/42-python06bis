from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory
from ex4 import (
    AggressiveStrategy,
    BattleStrategy,
    InvalidStrategyError,
    NormalStrategy,
)


def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    fighters = []
    for factory, strategy in opponents:
        fighters.append((factory.create_base(), strategy))

    names = [f"({c.name}+{s.name})" for c, s in fighters]
    print(" [ " + ", ".join(names) + " ]")
    print("*** Tournament ***")
    print(f"{len(fighters)} opponents involved")

    try:
        for i in range(len(fighters)):
            for j in range(i + 1, len(fighters)):
                creature1, strategy1 = fighters[i]
                creature2, strategy2 = fighters[j]
                print()
                print("* Battle *")
                print(creature1.describe())
                print(" vs.")
                print(creature2.describe())
                print(" now fight!")
                strategy1.act(creature1)
                strategy2.act(creature2)
    except InvalidStrategyError as error:
        print(f"Battle error, aborting tournament: {error}")


def main() -> None:
    flame_factory = FlameFactory()
    transform_factory = TransformCreatureFactory()
    normal = NormalStrategy()
    aggressive = AggressiveStrategy()

    print("Tournament 0 (basic)")
    battle([(flame_factory, normal), (transform_factory, aggressive)])
    print()
    print("Tournament 1 (error)")
    battle([(transform_factory, aggressive), (flame_factory, aggressive)])


if __name__ == "__main__":
    main()

from ex3 import TransformCreatureFactory
from ex3.capability import TransformCapability
from ex3.creature import Creature


def test_transform(creature: Creature) -> None:
    print(creature.describe())
    print(creature.attack())
    if isinstance(creature, TransformCapability):
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())


def main() -> None:
    print("Testing Creature with transform capability")
    factory = TransformCreatureFactory()
    print(" base:")
    test_transform(factory.create_base())
    print(" evolved:")
    test_transform(factory.create_evolved())


if __name__ == "__main__":
    main()

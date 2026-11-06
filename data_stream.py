#!/usr/bin/env python3

from typing import Any
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.items: list[tuple[int, str]] = []
        self.rank = 0

    def output(self) -> tuple[int, str]:
        if not self.items:
            raise IndexError("No index 0")
        return self.items.pop(0)

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Numeric Processor")

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, (int, float)):
            self.items.append((self.rank, str(data)))
            self.rank += 1
        else:
            for chunk in data:
                self.items.append((self.rank, str(chunk)))
                self.rank += 1

    @staticmethod
    def is_number(data: Any) -> bool:
        if isinstance(data, bool):
            return False
        if isinstance(data, (int, float)):
            return True
        else:
            return False

    def validate(self, data: Any) -> bool:
        if (
            isinstance(data, list)
            and all(self.is_number(chunk) for chunk in data)
        ):
            return True
        elif self.is_number(data):
            return True
        else:
            return False


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Text Processor")

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, str):
            self.items.append((self.rank, data))
            self.rank += 1
        else:
            for chunk in data:
                self.items.append((self.rank, chunk))
                self.rank += 1

    def validate(self, data: Any) -> bool:
        if isinstance(data, list) and all(isinstance(x, str)
                                          for x in data):
            return True
        elif isinstance(data, str):
            return True
        else:
            return False


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Log Processor")

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        if isinstance(data, dict):
            self.items.append((self.rank,
                               f"{data['log_level']}: {data['log_message']}"))
            self.rank += 1
        else:
            for chunk in data:
                self.items.append((self.rank, f"{chunk['log_level']}: "
                                              f"{chunk['log_message']}"))
                self.rank += 1

    @staticmethod
    def is_proper_dict(data: Any) -> bool:
        if (
            isinstance(data, dict)
            and all(isinstance(key, str)
                    and isinstance(val, str) for key, val in data.items())
            and 'log_level' in data
            and 'log_message' in data
        ):
            return True
        else:
            return False

    def validate(self, data: Any) -> bool:
        if isinstance(data, list) and all(self.is_proper_dict(chunk)
                                          for chunk in data):
            return True
        elif self.is_proper_dict(data):
            return True
        else:
            return False


class DataStream:
    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)

    def find_processor(self, element: Any) -> DataProcessor | None:
        for proc in self.processors:
            if proc.validate(element):
                return proc
        return None

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            proc = self.find_processor(element)
            if proc is None:
                print("DataStream error - "
                      f"Can't process element in stream: {element}")
            else:
                proc.ingest(element)

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self.processors:
            print("No processor found, no data")
        for proc in self.processors:
            print(f"{proc.name}: total {proc.rank} items processed, "
                  f"remaining {len(proc.items)} on processor")


def main() -> None:
    print("=== Code Nexus - Data Stream ===")
    print()
    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()
    print()

    print("Registering Numeric Processor")
    numeric = NumericProcessor()
    stream.register_processor(numeric)
    print()

    batch: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {"log_level": "WARNING",
             "log_message": "Telnet access! Use ssh instead"},
            {"log_level": "INFO", "log_message": "User wil is connected"},
        ],
        42,
        ["Hi", "five"],
    ]
    print(f"Send first batch of data on stream: {batch}")
    stream.process_stream(batch)
    stream.print_processors_stats()
    print()

    print("Registering other data processors")
    text = TextProcessor()
    log = LogProcessor()
    stream.register_processor(text)
    stream.register_processor(log)
    print("Send the same batch again")
    stream.process_stream(batch)
    stream.print_processors_stats()
    print()

    print("Consume some elements from the data processors: "
          "Numeric 3, Text 2, Log 1")
    for _ in range(3):
        numeric.output()
    for _ in range(2):
        text.output()
    log.output()
    stream.print_processors_stats()


if __name__ == "__main__":
    main()

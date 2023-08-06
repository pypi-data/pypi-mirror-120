import csv
import enum
from typing import Generator, Generic, Iterable, List, Optional, Type, TypeVar

import pkg_resources

from wilddog.models import transactions

T = TypeVar("T")

TEST_DATA_DIR = pkg_resources.resource_filename("tests", "data")


class TestDataType(enum.Enum):
    CSV = "csv"  # first line will be used for headers


class TestDataFile(Generic[T]):
    def __init__(self, name: str, data_type: TestDataType = TestDataType.CSV) -> None:
        self.name = f"{TEST_DATA_DIR}/{name}"
        self.data_type = data_type

    def _read_csv(self, return_type: Type[T]) -> Generator[T, None, None]:
        with open(self.name, "r") as f:
            for entry in csv.DictReader(f):
                yield return_type(**entry)

    def read(self, return_type: Type[T]) -> Generator[T, None, None]:
        generator: Optional[Generator[T, None, None]] = None

        if self.data_type == TestDataType.CSV:
            generator = self._read_csv(return_type)

        yield from generator


class TestDataResourceFixture(Generic[T]):
    def __init__(self, resource_name: str, return_type: Type[T]) -> None:
        self.return_type = return_type
        self.resource_name = resource_name

        self.entries: List[int] = []

    def pre(self) -> List[int]:
        resource = TestDataFile(self.resource_name)
        with transactions.Session() as s:
            for entry in resource.read(self.return_type):
                s.add(entry)

                # autogenerate id
                s.flush()
                self.entries.append(entry.id)
        return self.entries

    def post(self):
        with transactions.Session() as s:
            for t in self.entries:
                entry = s.query(self.return_type).get(t)
                s.delete(entry)

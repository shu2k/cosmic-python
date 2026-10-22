import pytest
from adapters import repository
from service_layer import services, unit_of_work


class FakeRepository(repository.AbstractRepository):
    def __init__(self, batches):
        self._batches = set(batches)

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True

class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.batches = FakeRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_add_batch():
    uow = FakeUnitOfWork()  #(3)
    services.add_batch("b1", "CRUNCHY-ARMCHAIR", 100, None, uow)  #(3)
    assert uow.batches.get("b1") is not None
    assert uow.committed


def test_allocate_returns_allocation():
    uow = FakeUnitOfWork()  #(3)
    services.add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow)  #(3)
    result = services.allocate("o1", "COMPLICATED-LAMP", 10, uow)  #(3)
    assert result == "batch1"
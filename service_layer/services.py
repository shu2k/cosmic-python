from datetime import date
from typing import Optional

from domain import model
from domain.model import OrderLine
from adapters.repository import AbstractRepository


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def allocate(orderid: str, sku: str, qty: int, repo: AbstractRepository, session) -> str:
    line = OrderLine(orderid=orderid, sku=sku, qty=qty)
    batches = repo.list()  # (1)
    if not is_valid_sku(sku, batches):  # (2)
        raise InvalidSku(f"Invalid sku {sku}")
    batchref = model.allocate(line, batches)  # (3)
    session.commit()  # (4)
    return batchref


def add_batch(
        ref: str, sku: str, qty: int, eta: Optional[date],
        repo: AbstractRepository, session,
) -> None:
    repo.add(model.Batch(ref, sku, qty, eta))
    session.commit()

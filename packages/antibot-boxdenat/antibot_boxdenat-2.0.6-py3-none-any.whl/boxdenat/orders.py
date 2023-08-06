from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Iterator
from uuid import uuid4

from antibot.tools import today
from antibot.user import User
from boxdenat.menu.model import Box, DessertWithFlavor, Soup, Drink
from injector import inject
from pyckson import rename, serialize, parse
from pymongo.database import Database


@rename(id='_id')
@dataclass
class Order:
    id: str
    user: User
    date: datetime
    complete: bool = False
    in_edition: bool = True
    boxes: List[Box] = field(default_factory=list)
    desserts: List[DessertWithFlavor] = field(default_factory=list)
    points_given: int = 0
    soups: List[Soup] = field(default_factory=list)
    drinks: List[Drink] = field(default_factory=list)

    def all_items(self):
        return self.boxes + self.desserts + self.soups + self.drinks


class OrderRepository:
    @inject
    def __init__(self, db: Database):
        self.collection = db['box_orders']

    def create(self, user: User) -> Order:
        order = Order(str(uuid4()), user, today())
        self.collection.insert_one(serialize(order))
        return order

    def update(self, order: Order):
        self.collection.replace_one({'_id': order.id}, serialize(order))

    def get(self, order_id: str) -> Optional[Order]:
        document = self.collection.find_one({'_id': order_id})
        if document is None:
            return None
        return parse(Order, document)

    def delete(self, order_id: str):
        self.collection.delete_one({'_id': order_id})

    def find_all(self, date: datetime) -> Iterator[Order]:
        for doc in self.collection.find({'date': date}):
            yield parse(Order, doc)

    def find(self, date: datetime, user: User) -> Optional[Order]:
        document = self.collection.find_one({'date': date, 'user.id': user.id})
        if document is None:
            return None
        return parse(Order, document)

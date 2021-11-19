import asyncio
import random


class Inventory:
    def __init__(self):
        self.catalogue = {
            "Burgers": [
                {"id": 1, "name": "Python Burger", "price": 5.99},
                {"id": 2, "name": "C Burger", "price": 4.99},
                {"id": 3, "name": "Ruby Burger", "price": 6.49},
                {"id": 4, "name": "Go Burger", "price": 5.99},
                {"id": 5, "name": "C++ Burger", "price": 7.99},
                {"id": 6, "name": "Java Burger", "price": 7.99}
            ],
            "Sides": {
                "Fries": [
                    {"id": 7, "size": "Small", "price": 2.49}, 
                    {"id": 8, "size": "Medium", "price": 3.49}, 
                    {"id": 9, "size": "Large", "price": 4.29}
                ],
                "Caesar Salad": [
                    {"id": 10, "size": "Small", "price": 3.49}, 
                    {"id": 11, "size": "Large", "price": 4.49}
                ]
            },
            "Drinks": {
                "Coke": [
                    {"id": 12, "size": "Small", "price": 1.99}, 
                    {"id": 13, "size": "Medium", "price": 2.49}, 
                    {"id": 14, "size": "Large", "price": 2.99}
                ],
                "Ginger Ale": [
                    {"id": 15, "size": "Small", "price": 1.99}, 
                    {"id": 16, "size": "Medium", "price": 2.49}, 
                    {"id": 17, "size": "Large", "price": 2.99}
                ],
                "Chocolate Milk Shake": [
                    {"id": 18, "size": "Small", "price": 3.99}, 
                    {"id": 19, "size": "Medium", "price": 4.49}, 
                    {"id": 20, "size": "Large", "price": 4.99}
                ]
            }
        }
        self._generate_item_lookup_dict()
        self.stock = {i + 1: random.randint(0,15) for i in range(len(self.items))}
        self.stock_lock = asyncio.Lock()

    def _generate_item_lookup_dict(self):
        self.items = {}
        for category in self.catalogue:
            category_collection = self.catalogue[category]

            if isinstance(category_collection, list):
                for item in category_collection:
                    new_item = item.copy()
                    new_item["category"] = category
                    new_item["subcategory"] = None
                    self.items[new_item["id"]] = new_item
            else:
                for subcategory in category_collection:
                    for item in category_collection[subcategory]:
                        new_item = item.copy()
                        new_item["category"] = category
                        new_item["subcategory"] = subcategory
                        self.items[new_item["id"]] = new_item

    def _verify_item_id(func):
        async def wrapper(self, item_id):
            if item_id not in self.stock:
                raise ValueError(f"No item with id: {item_id} exists in the inventory.")
            
            result = await func(self, item_id)
            return result
        
        return wrapper

    async def get_number_of_items(self):
        await asyncio.sleep(1)
        return len(self.items)
    
    async def get_catalogue(self):
        await asyncio.sleep(2)
        return self.catalogue

    @_verify_item_id
    async def get_stock(self, item_id):
        if item_id not in self.stock:
            raise ValueError(f"No item with id: {item_id} exists in the inventory.")
        await asyncio.sleep(2)

        async with self.stock_lock:
            return self.stock[item_id]

    @_verify_item_id
    async def decrement_stock(self, item_id):
        if item_id not in self.stock:
            raise ValueError(f"No item with id: {item_id} exists in the inventory.")

        if self.stock[item_id] == 0:
            return False
        
        async with self.stock_lock:
            self.stock[item_id] -= 1
            return True

    @_verify_item_id
    async def get_item(self, item_id):
        await asyncio.sleep(1)
        return self.items[item_id]
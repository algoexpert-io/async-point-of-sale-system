import asyncio
from combo import Combo


class Order:
    def __init__(self, inventory):
        self.inventory = inventory
        self.items_by_category = {"Burgers": [], "Sides": [], "Drinks": []}
        self.combos = []

    async def add_item(self, item_id):
        stock_level, item = await asyncio.gather(
            self.inventory.get_stock(item_id), self.inventory.get_item(item_id)
        )

        if stock_level == 0:
            return False, item_id

        success = await self.inventory.decrement_stock(item_id)
        # This may not be successful because in the time we waited
        # to get the stock and item the stock level may have decreased.
        if not success:
            return False, item_id

        self.items_by_category[item["category"]].append(item)

        return True, item_id

    def find_combos(self):
        number_of_combos = None

        for category_items in self.items_by_category.values():
            if number_of_combos == None:
                number_of_combos = len(category_items)
            else:
                number_of_combos = min(number_of_combos, len(category_items))

        self.items_by_category["Burgers"].sort(key=lambda x: x["price"])
        self.items_by_category["Sides"].sort(key=lambda x: x["price"])
        self.items_by_category["Drinks"].sort(key=lambda x: x["price"])

        for i in range(number_of_combos):
            burger = self.items_by_category["Burgers"].pop()
            side = self.items_by_category["Sides"].pop()
            drink = self.items_by_category["Drinks"].pop()
            combo = Combo(burger, side, drink)
            self.combos.append(combo)

    def get_price(self):
        self.find_combos()
        sub_total = 0

        for category in self.items_by_category.values():
            for item in category:
                sub_total += item["price"]

        for combo in self.combos:
            sub_total += combo.price

        return sub_total

    def __str__(self):
        string = ""

        for i, combo in enumerate(self.combos):
            string += str(combo)
            if i != len(self.combos) - 1:
                string += "\n"

        if len(self.combos) > 0:
            string += "\n"

        for category in self.items_by_category.values():
            for i, item in enumerate(category):
                name = item["name"] if "name" in item else item["size"]
                price = item["price"]
                subcategory = item["subcategory"]
                if subcategory == None:
                    subcategory = ""

                string += f"${price} {name} {subcategory}\n"

        return string[:-1]  # remove the last \n

class Combo:
    DISCOUNT = 0.15

    def __init__(self, burger, side, drink):
        self.burger = burger
        self.side = side
        self.drink = drink
        self.price = self._calculate_price()

    def _calculate_price(self):
        subtotal = self.burger["price"] + self.side["price"] + self.drink["price"] 
        return round(subtotal * (1 - Combo.DISCOUNT), 2)

    def __str__(self):
        string = f"${self.price} Burger Combo\n"
        string += f"  {self.burger['name']}\n"
        string += f"  {self.side['size']} {self.side['subcategory']}\n"
        string += f"  {self.drink['size']} {self.drink['subcategory']}"

        return string
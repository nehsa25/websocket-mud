from money import Money


class Inventory:
    items = []
    money = None

    def __init__(self, items=[], money=Money()):
        self.items = items
        self.money = money

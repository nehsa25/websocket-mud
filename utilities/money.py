class MoneyUtility:
    @staticmethod
    def get_coppers(coppers):
        # subtract drakes, gold, and silver from coppers
        return int(coppers % 1000 % 100 % 10)

    @staticmethod
    def get_silver(coppers):
        return int(coppers / 10)

    @staticmethod
    def get_gold(coppers):
        return int(coppers / 100)

    @staticmethod
    def get_drakes(coppers):
        return int(coppers / 1000)

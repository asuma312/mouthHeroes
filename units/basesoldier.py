from objects.units import baseunit


class basesoldier(baseunit):

    def __init__(self):
        super().__init__()
        self.color = 'red'
        self.image = None
        self.health = 100
        self.attack = 10
        self.defense = 10
        self.speed = 10


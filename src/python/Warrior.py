from Creature import Creature

class Warrior(Creature):
    def get_max_velocity(self):
        return 3.0

    max_velocity = property(get_max_velocity)

    def get_max_acceleration(self):
        return 10.0

    max_acceleration = property(get_max_acceleration)

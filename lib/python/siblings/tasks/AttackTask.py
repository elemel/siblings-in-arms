# Copyright 2007 Mikael Lind.

class AttackTask:
    def __init__(self, target):
        self.target = target

    def run(self, facade):
        yield 0.0

class TechTree(object):

    def __init__(self):
        self.__deps = {}

    def depends(self, cls, deps):
        self.__deps[cls] = tuple(deps)

    def veto(self, cls, force):
        deps = self.__deps[cls]
        return () if any(force.units[dep] for dep in deps) else deps

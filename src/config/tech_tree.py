from config.units import *
from TechTree import TechTree


tech_tree = TechTree()
 
# Building dependencies.
for cls, deps in [(Tavern, []),
                  (Farm, [Tavern, Inn, Hall]),
                  (Tower, [Tavern, Inn, Hall]),
                  (ArcheryRange, [Tavern, Inn, Hall]),
                  (Barracks, [Tavern, Inn, Hall]),
                  (Inn, [ArcheryRange, Barracks]),
                  (GamblingDen, [Inn, Hall]),
                  (Stables, [Inn, Hall]),
                  (Temple, [Inn, Hall]),
                  (Hall, [GamblingDen, Stables, Temple]),
                  (Laboratory, [Hall])]:
    tech_tree.depends(cls, deps)

# Unit dependencies.
for cls, deps in [(Monk, []),
                  (Ranger, [ArcheryRange]),
                  (Warrior, [Barracks]),
                  (Thief, [GamblingDen]),
                  (Knight, [Stables]),
                  (Priest, [Temple]),
                  (Wizard, [Laboratory])]:
    tech_tree.depends(cls, deps)
 

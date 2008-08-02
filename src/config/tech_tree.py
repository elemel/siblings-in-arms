from config.units import *
from TechTree import TechTree


tech_tree = TechTree()
 
# Building dependencies.
for cls, deps in [(Tavern, []),
                  (Farm, [Tavern]),
                  (ArcheryRange, [Tavern]),
                  (Tower, [ArcheryRange]),
                  (Barracks, [Tavern]),
                  (Temple, [Tavern]),
                  (Inn, [Barracks, Temple]),
                  (GamblingDen, [Inn]),
                  (Laboratory, [Inn]),
                  (Stables, [Inn]),
                  (Hall, [Laboratory, Stables])]:
    tech_tree.depends(cls, deps)

# Unit dependencies.
for cls, deps in [(Monk, []),
                  (Ranger, [ArcheryRange]),
                  (Warrior, [Barracks]),
                  (Priest, [Temple]),
                  (Thief, [GamblingDen]),
                  (Knight, [Stables]),
                  (Wizard, [Laboratory])]:
    tech_tree.depends(cls, deps)
 

import os

root = os.path.dirname(__file__)
while root != "/" and not os.path.isfile(os.path.join(root, "Jamroot")):
    root = os.path.dirname(root)

damage_factors = {
    ("knight", "ranger"): 0.5,
    ("knight", "warrior"): 1.5,
    ("ranger", "knight"): 1.5,
    ("ranger", "warrior"): 0.5,
    ("warrior", "knight"): 0.5,
    ("warrior", "ranger"): 1.5,
}

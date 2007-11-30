import os

root = os.path.dirname(__file__)
while root != "/" and not os.path.isfile(os.path.join(root, "Jamroot")):
    root = os.path.dirname(root)

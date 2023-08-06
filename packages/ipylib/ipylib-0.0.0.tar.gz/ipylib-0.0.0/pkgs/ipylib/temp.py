"""
This module is just temporoary.
Install those packages using 'pip install -r requirements.txt'
"""
print(f"{'*'*50} {__name__}\n{__doc__}")

import os
import sys

for p in ['idebug']:
    sys.path.append(f"{os.environ['HOME']}/pjts/{p}")

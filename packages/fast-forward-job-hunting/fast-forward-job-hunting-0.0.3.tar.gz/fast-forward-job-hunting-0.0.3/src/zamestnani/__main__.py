#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pathlib import Path
import os
import subprocess

print(__file__)

os.chdir(os.path.dirname(__file__))
print(f"Current directory: {Path.cwd()}")

#os.chmod('./selen_zamestnani.py', 0o755)
os.chmod('./centrala.py', 0o755)

#os.system("exec /path/to/another/script")

#import centrala
#exec(open("centrala.py").read())

#subprocess.call("./selen_zamestnani.py")
subprocess.call("./centrala.py")

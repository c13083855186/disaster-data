# app/tests/conftest.py

import sys
import os

# 获取项目根目录
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

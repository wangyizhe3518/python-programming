import sys
from pathlib import Path

file_dir = Path(__file__).resolve().parent
project_dir = file_dir.parent
sys.path.append(str(project_dir))

from regression import linear_regression, causal_regression  # noqa: F401 E402

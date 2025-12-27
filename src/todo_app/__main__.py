"""
Allow running todo_app as a module: python -m todo_app
"""
from todo_app.main import main
import sys

if __name__ == "__main__":
    sys.exit(main())

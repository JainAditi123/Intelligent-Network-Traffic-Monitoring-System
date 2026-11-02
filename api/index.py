import os
import sys

# Add project root directory to path so models, processed_data, and web_app are found
_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)

from web_app.app import app

# Vercel entry point
if __name__ == "__main__":
    app.run()

"""DIT 2026 Assessment — E-P-I-A-S x SAE Framework.

Run from inside the assessment directory:
    cd assessment
    python __main__.py
"""
import sys
from pathlib import Path

# Ensure this directory is on sys.path so local imports work
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app
from config import settings

app = create_app()
print(f"DIT Assessment starting on http://localhost:{settings.port}")
app.run(host='0.0.0.0', port=settings.port, debug=settings.debug)

import os, sys, pathlib, secrets, tempfile
os.environ.setdefault("JWT_SECRET", secrets.token_hex(32))
os.environ.setdefault("DB_PATH", os.path.join(tempfile.mkdtemp(), "import.db"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

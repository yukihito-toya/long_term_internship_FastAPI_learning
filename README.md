```ps
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r .\requirements.txt
docker compose up -d
```

```ps
uvicorn app_1744251140387:app --reload
```

```ps
pytest .\tests\test_1744685175533.py
```

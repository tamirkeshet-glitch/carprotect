# CarProtect Backend (FastAPI)

## התקנה
```bash
cd backend
pip install -r requirements.txt
```

## הרצה
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints
- `GET /` — מידע כללי
- `GET /vehicle/{plate}` — דוח רכב מלא  
  דוגמה: http://localhost:8000/vehicle/69918002
- `GET /health` — בדיקת תקינות
- `GET /docs` — Swagger UI

## דוגמה
```bash
curl http://localhost:8000/vehicle/69918002
```

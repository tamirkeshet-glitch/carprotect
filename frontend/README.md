# אב-טיפוס ווב פשוט

דף HTML בודד שמתחבר ל-backend.

## הרצה
1. הרץ את הבקאנד:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
2. פתח את `frontend/index.html` בדפדפן (או שרת אותו באמצעות `python -m http.server 3000` מתוך תיקיית frontend).

**הערה:** בקובץ `index.html` הכתובת `const API = "http://localhost:8000"`. שנה אם השרת רץ בכתובת אחרת.

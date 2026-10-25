# CarProtect

אפליקציה לבדיקת סטטוס רכב בישראל — צילום לוחית וקבלת דוח מלא ממקורות פתוחים.

המערכת שואבת נתונים ישירות ממאגרי משרד התחבורה ב-[data.gov.il](https://data.gov.il) (בלי תלות בצד ג' כמו דוח בלקר).

## מטרות
- כלי פשוט ומהיר לרוכשי רכב פרטיים ולסוחרי רכב.
- דוח בזמן אמת עם: מספר ידיים, בעלות חברה/ליסינג/השכרה, קמ אחרון, תוקף טסט, ריקולים, סטטוס פעיל.
- שאיבה ישירה מהמקור הממשלתי הפתוח.

## תוכן
- [תוכנית עבודה מלאה](./docs/WORK_PLAN.md)
- [מקורות נתונים](./docs/DATA_SOURCES.md)
- [ארכיטקטורה](./docs/ARCHITECTURE.md)
- [סקריפט CLI](./scripts/vehicle_report.py)
- [בקאנד FastAPI](./backend/)
- [אב-טיפוס ווב](./frontend/index.html)

## התקדמות
- [x] תיעוד תוכנית עבודה
- [x] סקריפט Python לשליפת דוח מלא
- [x] Backend FastAPI (`GET /vehicle/{plate}`)
- [x] אב-טיפוס ווב פשוט
- [ ] אפיון מסכים מובייל / אפליקציה מלאה

## הרצת אב-טיפוס
```bash
# טרמינל 1 — בקאנד
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# טרמינל 2 — פתח דפדפן
open frontend/index.html
# או: cd frontend && python -m http.server 3000
```

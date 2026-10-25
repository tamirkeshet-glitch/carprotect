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

## התקדמות
- [x] תיעוד תוכנית עבודה
- [x] סקריפט Python לשליפת דוח מלא
- [x] Backend FastAPI (`GET /vehicle/{plate}`)
- [ ] אפיון מסכים
- [ ] אב-טיפוס מובייל

## הרצת הבקאנד
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
# אז פתח: http://localhost:8000/docs
```

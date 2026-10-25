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
- [אב-טיפוס Flutter](./mobile/)

## התקדמות
- [x] תיעוד תוכנית עבודה
- [x] סקריפט Python לשליפת דוח מלא
- [x] Backend FastAPI
- [x] אב-טיפוס ווב
- [x] אב-טיפוס Flutter מובייל
- [ ] OCR לזיהוי לוחית
- [ ] שיפורים ופריסה

## הרצת אב-טיפוס Flutter
```bash
# בקאנד
cd backend && python -m uvicorn main:app --reload --host 0.0.0.0

# מובייל
cd mobile
flutter pub get
flutter run
```

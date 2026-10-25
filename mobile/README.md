# CarProtect Mobile (Flutter)

אב-טיפוס מובייל פשוט.

## דרישות
- Flutter SDK מותקן ([flutter.dev](https://flutter.dev))

## הרצה

1. הרץ את ה-backend:
   ```bash
   cd backend
   python -m uvicorn main:app --reload --host 0.0.0.0
   ```

2. בתיקיית mobile:
   ```bash
   cd mobile
   flutter pub get
   flutter run
   ```

## כתובת API
בקובץ `lib/main.dart` שנה את `apiBase`:
- Android emulator: `http://10.0.2.2:8000`
- iOS simulator: `http://localhost:8000`
- מכשיר אמיתי: כתובת IP של המחשב (למשל `http://192.168.1.10:8000`)

## בניית אפליקציה
```bash
flutter build apk      # Android
flutter build ios      # iOS (דורש Mac)
```

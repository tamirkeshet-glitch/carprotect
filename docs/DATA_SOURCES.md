# מקורות נתונים — data.gov.il

## Endpoint ראשי
```
GET https://data.gov.il/api/3/action/datastore_search
?resource_id=<RESOURCE_ID>
&filters={"mispar_rechev": <NUMBER>}
&limit=20
```

## Resource IDs עיקריים

| שם | Resource ID | תיאור |
|-----|-------------|--------|
| Active Private/Commercial | `053cea08-09bc-40ec-8f7a-156f0677aff3` | מאגר רכב פעיל עיקרי |
| Ownership History | `bb2355dc-9ec7-4f06-9c3f-3344672171da` | היסטוריית בעלויות (מ-2017) |
| Mileage + Changes | `56063a99-8a3e-4ff4-912e-5966c0279bad` | ק"מ אחרון + שינויי מבנה |
| Outstanding Recalls | `36bf1404-0be4-49d2-82dc-2f1ead4a8b93` | ריקולים שלא בוצעו |
| Inactive with model | `f6efe89a-fb3d-43a4-bb61-9bf12a9b9099` | לא פעילים |
| Final Cancel | `851ecab1-0622-4dbe-a6c7-f950cf82abf9` | ביטול סופי |

## שדות חשובים
- `baalut` / `baalut_dt` — סוג בעלות ותאריך
- `kilometer_test_aharon` — ק"מ אחרון
- `tokef_dt`, `mivchan_acharon_dt` — תוקף וטסט
- `tozeret_nm`, `degem_nm`, `shnat_yitzur`, `sug_delek_nm`

## דוגמת שאילתה (פייתון)
```python
import requests

def get_vehicle(plate: int):
    url = "https://data.gov.il/api/3/action/datastore_search"
    params = {
        "resource_id": "053cea08-09bc-40ec-8f7a-156f0677aff3",
        "filters": {"mispar_rechev": plate},
        "limit": 1
    }
    r = requests.get(url, params=params)
    return r.json()["result"]["records"]
```

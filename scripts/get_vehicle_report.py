#!/usr/bin/env python3
"""
CarProtect — שליפת דוח רכב מלא ממאגרי data.gov.il
שימוש: python get_vehicle_report.py 69918002
"""

import sys
import json
import requests
from typing import Optional, Dict, Any, List

API_URL = "https://data.gov.il/api/3/action/datastore_search"

RESOURCES = {
    "active": "053cea08-09bc-40ec-8f7a-156f0677aff3",
    "ownership": "bb2355dc-9ec7-4f06-9c3f-3344672171da",
    "mileage": "56063a99-8a3e-4ff4-912e-5966c0279bad",
    "recalls": "36bf1404-0be4-49d2-82dc-2f1ead4a8b93",
    "inactive": "f6efe89a-fb3d-43a4-bb61-9bf12a9b9099",
    "final_cancel": "851ecab1-0622-4dbe-a6c7-f950cf82abf9",
}

def query(resource_id: str, plate: int, limit: int = 20, filter_field: str = "mispar_rechev") -> List[Dict]:
    """שאילה גנרית ל-data.gov.il"""
    filters = {filter_field: plate}
    params = {
        "resource_id": resource_id,
        "filters": json.dumps(filters),
        "limit": limit,
    }
    try:
        r = requests.get(API_URL, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        if data.get("success") and data.get("result"):
            return data["result"].get("records", [])
    except Exception as e:
        print(f"Error querying {resource_id}: {e}", file=sys.stderr)
    return []

def get_vehicle_report(plate: int) -> Dict[str, Any]:
    """מחזיר דוח מסודר לרכב"""
    report: Dict[str, Any] = {
        "plate": plate,
        "found": False,
        "basic": {},
        "ownership_history": [],
        "ownership_summary": {},
        "mileage": {},
        "recalls": [],
        "status": "unknown",
        "flags": [],
    }

    # 1. מאגר פעיל
    active = query(RESOURCES["active"], plate, limit=1)
    if active:
        report["found"] = True
        report["status"] = "active"
        b = active[0]
        report["basic"] = {
            "manufacturer": b.get("tozeret_nm"),
            "model": b.get("kinuy_mishari") or b.get("degem_nm"),
            "year": b.get("shnat_yitzur"),
            "color": b.get("tzeva_rechev"),
            "fuel": b.get("sug_delek_nm"),
            "trim": b.get("ramat_gimur"),
            "current_ownership": b.get("baalut"),
            "vin": b.get("misgeret"),
            "last_test": b.get("mivchan_acharon_dt"),
            "license_expiry": b.get("tokef_dt"),
            "first_registration": b.get("moed_aliya_lakvish"),
        }

    # 2. היסטוריית בעלויות
    ownership = query(RESOURCES["ownership"], plate, limit=50)
    if ownership:
        ownership_sorted = sorted(ownership, key=lambda x: x.get("baalut_dt", 0))
        report["ownership_history"] = [
            {"date": str(o.get("baalut_dt")), "type": o.get("baalut")} for o in ownership_sorted
        ]

        types = [o.get("baalut", "") for o in ownership]
        company_keywords = ["חברה", "החכר", "השכרה", "סוחר", "ליסינג"]
        had_company = any(any(kw in t for kw in company_keywords) for t in types)

        report["ownership_summary"] = {
            "number_of_owners": len(set(types)) or len(ownership),
            "records": len(ownership),
            "had_company_or_leasing": had_company,
            "types_seen": list(set(types)),
        }
        if had_company:
            report["flags"].append("היה בעלות חברה/ליסינג/השכרה/סוחר")

    # 3. קמ
    mileage_recs = query(RESOURCES["mileage"], plate, limit=1)
    if mileage_recs:
        m = mileage_recs[0]
        report["mileage"] = {
            "last_km": m.get("kilometer_test_aharon"),
            "structure_change": bool(m.get("shinui_mivne_ind")),
            "lpg": bool(m.get("gapam_ind")),
            "color_change": bool(m.get("shnui_zeva_ind")),
            "origin": m.get("mkoriut_nm") or None,
            "first_registration_date": m.get("rishum_rishon_dt"),
        }

    # 4. ריקולים
    recalls = query(RESOURCES["recalls"], plate, limit=10, filter_field="MISPAR_RECHEV")
    if recalls:
        report["recalls"] = [
            {
                "id": r.get("RECALL_ID"),
                "type": r.get("SUG_RECALL"),
                "description": r.get("TEUR_TAKALA"),
                "opened": r.get("TAARICH_PTICHA"),
            }
            for r in recalls
        ]
        report["flags"].append(f"יש {len(recalls)} ריקולים פתוחים")

    # 5. סטטוס לא פעיל
    if not report["found"]:
        inactive = query(RESOURCES["inactive"], plate, limit=1)
        final = query(RESOURCES["final_cancel"], plate, limit=1)
        if final:
            report["status"] = "final_cancellation"
            report["flags"].append("ביטול סופי / ירד מהכביש")
        elif inactive:
            report["status"] = "inactive"
            report["flags"].append("לא פעיל (חסר תוקף)")

    return report

def print_report(report: Dict):
    """הדפסה ידידותית למסך"""
    print("=" * 60)
    print(f"דוח רכב מספר: {report['plate']}")
    print("=" * 60)

    if not report["found"] and report["status"] == "unknown":
        print("הרכב לא נמצא במאגרים הפתוחים.")
        return

    b = report["basic"]
    if b:
        print(f"יצרן:     {b.get('manufacturer')}")
        print(f"דגם:      {b.get('model')}")
        print(f"שנה:      {b.get('year')}")
        print(f"צבע:      {b.get('color')}")
        print(f"דלק:      {b.get('fuel')}")
        print(f"בעלות נוכחית: {b.get('current_ownership')}")
        print(f"טסט אחרון: {b.get('last_test')}")
        print(f"תוקף רישיון: {b.get('license_expiry')}")
        print()

    if report["mileage"]:
        km = report["mileage"].get("last_km")
        if km:
            print(f"קמ אחרון: {km:,} קמ")
        else:
            print("קמ: לא זמין")
        print()

    if report["ownership_history"]:
        print("היסטוריית בעלויות:")
        for o in report["ownership_history"]:
            print(f"  {o['date']} — {o['type']}")
        summary = report["ownership_summary"]
        print(f"סהכ רשומות: {summary.get('records')}")
        if summary.get("had_company_or_leasing"):
            print("היה בעלות חברה/ליסינג/השכרה")
        print()

    if report["recalls"]:
        print(f"ריקולים פתוחים: {len(report['recalls'])}")
        for r in report["recalls"]:
            print(f"  - {r.get('description')}")
        print()

    print(f"סטטוס: {report['status']}")
    if report["flags"]:
        print("דגלים:")
        for f in report["flags"]:
            print(f"  * {f}")

    print("=" * 60)

def main():
    if len(sys.argv) < 2:
        print("שימוש: python get_vehicle_report.py <מספר_רכב>")
        print("דוגמה: python get_vehicle_report.py 69918002")
        sys.exit(1)

    try:
        plate = int(sys.argv[1].replace("-", ""))
    except ValueError:
        print("מספר רכב לא תקין")
        sys.exit(1)

    report = get_vehicle_report(plate)
    print_report(report)

    if "--json" in sys.argv:
        print("\n--- JSON ---")
        print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

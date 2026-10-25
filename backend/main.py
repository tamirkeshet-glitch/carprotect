"""
CarProtect Backend - FastAPI
Run: uvicorn main:app --reload
"""

import json
import requests
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CarProtect API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    except Exception:
        pass
    return []

def build_report(plate: int) -> Dict[str, Any]:
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
            "records": len(ownership),
            "had_company_or_leasing": had_company,
            "types_seen": list(set(types)),
        }
        if had_company:
            report["flags"].append("had_company_or_leasing")

    mileage_recs = query(RESOURCES["mileage"], plate, limit=1)
    if mileage_recs:
        m = mileage_recs[0]
        report["mileage"] = {
            "last_km": m.get("kilometer_test_aharon"),
            "structure_change": bool(m.get("shinui_mivne_ind")),
            "lpg": bool(m.get("gapam_ind")),
            "color_change": bool(m.get("shnui_zeva_ind")),
            "origin": m.get("mkoriut_nm") or None,
        }

    recalls = query(RESOURCES["recalls"], plate, limit=10, filter_field="MISPAR_RECHEV")
    if recalls:
        report["recalls"] = [
            {
                "id": r.get("RECALL_ID"),
                "description": r.get("TEUR_TAKALA"),
                "opened": r.get("TAARICH_PTICHA"),
            }
            for r in recalls
        ]
        report["flags"].append(f"{len(recalls)}_open_recalls")

    if not report["found"]:
        if query(RESOURCES["final_cancel"], plate, limit=1):
            report["status"] = "final_cancellation"
            report["flags"].append("final_cancellation")
        elif query(RESOURCES["inactive"], plate, limit=1):
            report["status"] = "inactive"
            report["flags"].append("inactive")

    return report

@app.get("/")
def root():
    return {"service": "CarProtect", "docs": "/docs", "example": "/vehicle/69918002"}

@app.get("/vehicle/{plate}")
def get_vehicle(plate: int):
    """מחזיר דוח מלא לרכב לפי מספר רישוי"""
    if plate < 1000000 or plate > 99999999:
        raise HTTPException(status_code=400, detail="Invalid plate number")
    report = build_report(plate)
    if not report["found"] and report["status"] == "unknown":
        raise HTTPException(status_code=404, detail="Vehicle not found in open datasets")
    return report

@app.get("/health")
def health():
    return {"status": "ok"}

#!/usr/bin/env python3
"""CarProtect vehicle report from data.gov.il. Usage: python vehicle_report.py 69918002"""
import sys, json, requests
from typing import Dict, Any, List

API = "https://data.gov.il/api/3/action/datastore_search"
RES = {
    "active": "053cea08-09bc-40ec-8f7a-156f0677aff3",
    "ownership": "bb2355dc-9ec7-4f06-9c3f-3344672171da",
    "mileage": "56063a99-8a3e-4ff4-912e-5966c0279bad",
    "recalls": "36bf1404-0be4-49d2-82dc-2f1ead4a8b93",
    "inactive": "f6efe89a-fb3d-43a4-bb61-9bf12a9b9099",
    "final": "851ecab1-0622-4dbe-a6c7-f950cf82abf9",
}

def q(rid, plate, lim=20, field="mispar_rechev"):
    try:
        r = requests.get(API, params={"resource_id": rid, "filters": json.dumps({field: plate}), "limit": lim}, timeout=15)
        d = r.json()
        return d.get("result", {}).get("records", []) if d.get("success") else []
    except:
        return []

def report(plate: int) -> Dict[str, Any]:
    out = {"plate": plate, "found": False, "basic": {}, "ownership": [], "mileage": {}, "recalls": [], "status": "unknown", "flags": []}
    act = q(RES["active"], plate, 1)
    if act:
        out["found"] = True
        out["status"] = "active"
        b = act[0]
        out["basic"] = {k: b.get(v) for k,v in {
            "manufacturer":"tozeret_nm","model":"kinuy_mishari","year":"shnat_yitzur",
            "color":"tzeva_rechev","fuel":"sug_delek_nm","ownership":"baalut",
            "last_test":"mivchan_acharon_dt","expiry":"tokef_dt"}.items()}
    own = q(RES["ownership"], plate, 50)
    if own:
        out["ownership"] = sorted([{"date": str(o.get("baalut_dt")), "type": o.get("baalut")} for o in own], key=lambda x: x["date"])
        types = [o.get("baalut","") for o in own]
        if any(any(k in t for k in ["חברה","החכר","השכרה","סוחר"]) for t in types):
            out["flags"].append("company or leasing ownership")
    mil = q(RES["mileage"], plate, 1)
    if mil:
        out["mileage"] = {"last_km": mil[0].get("kilometer_test_aharon")}
    rec = q(RES["recalls"], plate, 10, "MISPAR_RECHEV")
    if rec:
        out["recalls"] = [{"desc": r.get("TEUR_TAKALA")} for r in rec]
        out["flags"].append(f"{len(rec)} open recalls")
    if not out["found"]:
        if q(RES["final"], plate, 1): out["status"] = "final_cancel"
        elif q(RES["inactive"], plate, 1): out["status"] = "inactive"
    return out

def show(r):
    print("="*50)
    print("Plate:", r["plate"], "| Status:", r["status"])
    if r["basic"]:
        for k,v in r["basic"].items():
            print(f"{k}: {v}")
    if r["mileage"].get("last_km"):
        print("Last km:", f"{r['mileage']['last_km']:,}")
    if r["ownership"]:
        print("Ownership:")
        for o in r["ownership"]: print(" ", o["date"], o["type"])
    if r["flags"]: print("Flags:", ", ".join(r["flags"]))
    print("="*50)

if __name__ == "__main__":
    if len(sys.argv)<2: print("Usage: python vehicle_report.py <plate>"); sys.exit(1)
    p = int(sys.argv[1].replace("-",""))
    rep = report(p)
    show(rep)
    if "--json" in sys.argv: print(json.dumps(rep, ensure_ascii=False, indent=2))

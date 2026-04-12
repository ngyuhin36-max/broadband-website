"""Fetch HK government's Licensed Hotels & Guesthouses data.
Source: Office of the Licensing Authority (OLA), Home Affairs Department.
data.gov.hk publishes this as CSV.
"""
import urllib.request, urllib.parse, csv, io, json
from pathlib import Path

# Known URL pattern for the licensed-hotels CSV (may change over time)
URLS = [
    "https://www.hadla.gov.hk/filemanager/content/ola/hotel/licensed_hotel_list_chi.csv",
    "https://www.hadla.gov.hk/filemanager/content/ola/hotel/licensed_hotel_list_eng.csv",
    "https://www.hadla.gov.hk/tc/content/ola/hotel/licensed_hotel_list_chi.csv",
    "https://www.hadla.gov.hk/filemanager/content/ola/hotel/hotel_chi.csv",
    "https://www.hadla.gov.hk/filemanager/content/ola/hotel/hotel_eng.csv",
]

for u in URLS:
    try:
        print(f"trying {u}")
        req = urllib.request.Request(u, headers={"User-Agent":"Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=20).read()
        print(f"  got {len(data)} bytes")
        # Try decoding
        for enc in ("utf-8","big5","gbk"):
            try:
                text = data.decode(enc)
                print(f"  decoded as {enc}, first 500: {text[:500]}")
                Path(f"gov_hotels_{enc}.csv").write_bytes(data)
                break
            except Exception: pass
        break
    except Exception as e:
        print(f"  err: {e}")

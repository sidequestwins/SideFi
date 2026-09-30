#!/usr/bin/env python3
"""Build a sanitized SideFi sample: replaces real transaction data in the
exported dashboard HTML with coherent fake data, and adjusts hardcoded copy.

Reads:  ~/workspace/your_files/monthly-spending/monthly-spending.html
Writes: ~/workspace/sidefi/index.html
"""
import base64
import json
import re
from pathlib import Path

SRC = Path.home() / "workspace/your_files/monthly-spending/monthly-spending.html"
DST = Path.home() / "workspace/sidefi/index.html"

# ---------------------------------------------------------------- sample data
# (date, merchant, descriptor, amount, category, account, location, time)
SPEND = {
    "2026-07": [
        ("2026-07-01", "Sample Property Mgmt", "SAMPLE PROPERTY MGMT RENT", 2400.00, "RENT_AND_UTILITIES", "Sample Checking …0001", "New York NY", "2026-07-01T09:00:00Z"),
        ("2026-07-03", "Bluebird Coffee", "BLUEBIRD COFFEE", 6.50, "FOOD_AND_DRINK", "Sample Card …0002", "New York NY", "2026-07-03T14:22:10Z"),
        ("2026-07-05", "Green Grocer", "GREEN GROCER #12", 84.20, "FOOD_AND_DRINK", "Sample Card …0002", "New York NY", None),
        ("2026-07-06", "StreamFlix", "STREAMFLIX.COM", 15.99, "SUBSCRIPTIONS", "Sample Card …0002", None, None),
        ("2026-07-08", "Metro Transit", "MTA*MTA", 34.00, "TRANSPORTATION", "Sample Card …0002", "New York NY", None),
        ("2026-07-10", "Sample Law Firm", "SAMPLE LAW FIRM PC", 450.00, "LAWYERS", "Sample Card …0003", "Irvine CA", "2026-07-10T16:05:44Z"),
        ("2026-07-12", "Taco Libre", "TACO LIBRE", 22.75, "FOOD_AND_DRINK", "Sample Card …0002", "New York NY", None),
        ("2026-07-14", "City Power & Light", "CITY POWER & LIGHT", 118.42, "RENT_AND_UTILITIES", "Sample Checking …0001", None, None),
        ("2026-07-15", "SampleMart", "SAMPLEMART.COM", 63.10, "GENERAL_MERCHANDISE", "Sample Card …0002", None, "2026-07-15T19:31:02Z"),
        ("2026-07-18", "Grand Cinema", "GRAND CINEMA", 32.00, "ENTERTAINMENT", "Sample Card …0002", "New York NY", None),
        ("2026-07-20", "City Parking (parking)", "CITY PARKING GARAGE", 28.00, "TRANSPORTATION", "Sample Card …0002", "New York NY", "2026-07-20T12:15:00Z"),
        ("2026-07-22", "Sushi Naka", "SUSHI NAKA", 58.40, "FOOD_AND_DRINK", "Sample Card …0003", "New York NY", None),
        ("2026-07-25", "MusicFlow", "MUSICFLOW", 10.99, "SUBSCRIPTIONS", "Sample Card …0002", None, None),
        ("2026-07-27", "Clip Joint", "CLIP JOINT BARBER", 35.00, "PERSONAL_CARE", "Sample Card …0002", "New York NY", None),
        ("2026-07-29", "Book Nook", "BOOK NOOK", 27.95, "GENERAL_MERCHANDISE", "Sample Card …0002", None, None),
    ],
    "2026-08": [
        ("2026-08-01", "Sample Property Mgmt", "SAMPLE PROPERTY MGMT RENT", 2400.00, "RENT_AND_UTILITIES", "Sample Checking …0001", "New York NY", "2026-08-01T09:00:00Z"),
        ("2026-08-02", "Harbor Hotel", "HARBOR HOTEL", 289.00, "TRAVEL", "Sample Card …0003", "Boston MA", "2026-08-02T15:00:00Z"),
        ("2026-08-04", "Bluebird Coffee", "BLUEBIRD COFFEE", 6.50, "FOOD_AND_DRINK", "Sample Card …0002", "New York NY", None),
        ("2026-08-06", "StreamFlix", "STREAMFLIX.COM", 15.99, "SUBSCRIPTIONS", "Sample Card …0002", None, None),
        ("2026-08-07", "Sample Airlines", "SAMPLE AIRLINES", 214.60, "TRAVEL", "Sample Card …0003", None, "2026-08-07T11:20:00Z"),
        ("2026-08-09", "Green Grocer", "GREEN GROCER #12", 91.33, "FOOD_AND_DRINK", "Sample Card …0002", "New York NY", None),
        ("2026-08-11", "ChargePoint EV", "CHARGEPOINT EV", 18.75, "TRANSPORTATION", "Sample Card …0002", "New York NY", None),
        ("2026-08-13", "City Power & Light", "CITY POWER & LIGHT", 132.10, "RENT_AND_UTILITIES", "Sample Checking …0001", None, None),
        ("2026-08-15", "Hardware Haven", "HARDWARE HAVEN", 74.28, "HOME_IMPROVEMENT", "Sample Card …0002", "New York NY", None),
        ("2026-08-17", "Taco Libre", "TACO LIBRE", 19.50, "FOOD_AND_DRINK", "Sample Card …0002", "New York NY", None),
        ("2026-08-19", "City Dental", "CITY DENTAL", 120.00, "MEDICAL", "Sample Card …0003", "New York NY", "2026-08-19T10:30:00Z"),
        ("2026-08-21", "SampleMart", "SAMPLEMART.COM", 45.99, "GENERAL_MERCHANDISE", "Sample Card …0002", None, None),
        ("2026-08-23", "Grand Cinema", "GRAND CINEMA", 32.00, "ENTERTAINMENT", "Sample Card …0002", "New York NY", None),
        ("2026-08-25", "MusicFlow", "MUSICFLOW", 10.99, "SUBSCRIPTIONS", "Sample Card …0002", None, None),
        ("2026-08-27", "Wash & Fold", "WASH & FOLD LAUNDRY", 24.00, "GENERAL_SERVICES", "Sample Card …0002", "New York NY", None),
        ("2026-08-29", "Sushi Naka", "SUSHI NAKA", 61.20, "FOOD_AND_DRINK", "Sample Card …0003", "New York NY", None),
    ],
    "2026-09": [
        ("2026-09-01", "Sample Property Mgmt", "SAMPLE PROPERTY MGMT RENT", 2400.00, "RENT_AND_UTILITIES", "Sample Checking …0001", "New York NY", "2026-09-01T09:00:00Z"),
        ("2026-09-02", "Open Library Fund", "OPEN LIBRARY FUND DONATION", 25.00, "DONATIONS", "Sample Card …0002", None, None),
        ("2026-09-04", "Bluebird Coffee", "BLUEBIRD COFFEE", 6.50, "FOOD_AND_DRINK", "Sample Card …0002", "New York NY", None),
        ("2026-09-06", "StreamFlix", "STREAMFLIX.COM", 15.99, "SUBSCRIPTIONS", "Sample Card …0002", None, None),
        ("2026-09-08", "Green Grocer", "GREEN GROCER #12", 77.64, "FOOD_AND_DRINK", "Sample Card …0002", "New York NY", None),
        ("2026-09-10", "Sample Law Firm", "SAMPLE LAW FIRM PC", 450.00, "LAWYERS", "Sample Card …0003", "Irvine CA", "2026-09-10T16:05:44Z"),
        ("2026-09-12", "Taco Libre", "TACO LIBRE", 24.30, "FOOD_AND_DRINK", "Sample Card …0002", "New York NY", None),
        ("2026-09-14", "City Power & Light", "CITY POWER & LIGHT", 121.55, "RENT_AND_UTILITIES", "Sample Checking …0001", None, None),
        ("2026-09-15", "Sample Air Conditioners", "SAMPLE AIR CONDITIONERS", 899.00, "HOME_IMPROVEMENT", "Sample Card …0003", None, "2026-09-15T13:45:00Z"),
        ("2026-09-17", "Metro Transit", "MTA*MTA", 34.00, "TRANSPORTATION", "Sample Card …0002", "New York NY", None),
        ("2026-09-19", "Sushi Naka", "SUSHI NAKA", 55.80, "FOOD_AND_DRINK", "Sample Card …0003", "New York NY", None),
        ("2026-09-21", "Grand Cinema", "GRAND CINEMA", 32.00, "ENTERTAINMENT", "Sample Card …0002", "New York NY", None),
        ("2026-09-23", "City Parking (parking)", "CITY PARKING GARAGE", 28.00, "TRANSPORTATION", "Sample Card …0002", "New York NY", "2026-09-23T12:15:00Z"),
        ("2026-09-25", "MusicFlow", "MUSICFLOW", 10.99, "SUBSCRIPTIONS", "Sample Card …0002", None, None),
        ("2026-09-27", "Clip Joint", "CLIP JOINT BARBER", 35.00, "PERSONAL_CARE", "Sample Card …0002", "New York NY", None),
        ("2026-09-29", "Book Nook", "BOOK NOOK", 31.50, "GENERAL_MERCHANDISE", "Sample Card …0002", None, None),
    ],
}

INCOME = {
    "2026-07": [
        ("2026-07-15", "Sample Employer", "SAMPLE EMPLOYER PAYROLL", 3250.00, "salary", "Sample Checking …0001", "2026-07-15T06:00:00Z"),
        ("2026-07-31", "Sample Employer", "SAMPLE EMPLOYER PAYROLL", 3250.00, "salary", "Sample Checking …0001", "2026-07-31T06:00:00Z"),
        ("2026-07-31", "Interest Earned", "Interest Earned", 4.12, "other", "Sample Savings …0004", None),
    ],
    "2026-08": [
        ("2026-08-15", "Sample Employer", "SAMPLE EMPLOYER PAYROLL", 3250.00, "salary", "Sample Checking …0001", "2026-08-15T06:00:00Z"),
        ("2026-08-31", "Sample Employer", "SAMPLE EMPLOYER PAYROLL", 3250.00, "salary", "Sample Checking …0001", "2026-08-31T06:00:00Z"),
        ("2026-08-31", "Interest Earned", "Interest Earned", 3.98, "other", "Sample Savings …0004", None),
    ],
    "2026-09": [
        ("2026-09-15", "Sample Employer", "SAMPLE EMPLOYER PAYROLL", 3250.00, "salary", "Sample Checking …0001", "2026-09-15T06:00:00Z"),
        ("2026-09-29", "Sample Employer", "SAMPLE EMPLOYER PAYROLL", 3250.00, "salary", "Sample Checking …0001", None),
        ("2026-09-30", "Interest Earned", "Interest Earned", 4.05, "other", "Sample Savings …0004", None),
    ],
}

REFUNDS = {
    "2026-09": [("2026-09-16", "SAMPLE AIR CONDITIONERS REFUND", -45.00)],
}

ANOMALIES = {
    "2026-09": [("2026-09-15", "Sample Air Conditioners", 899.00, "large single charge")],
}

EXCLUDED = {
    "2026-08": [("2026-08-20", "Duplicate Test Charge", 12.00, "test charge, never posted")],
}


def build_month(key, year, month_num, last_day):
    spend = [
        {"date": d, "merchant": m, "descriptor": desc, "amount": a,
         "category": c, "account": acct, "location": loc, "time": t}
        for (d, m, desc, a, c, acct, loc, t) in SPEND[key]
    ]
    income = [
        {"date": d, "merchant": m, "descriptor": desc, "amount": a,
         "kind": k, "account": acct, "time": t}
        for (d, m, desc, a, k, acct, t) in INCOME[key]
    ]
    by_category = {}
    for line in spend:
        by_category[line["category"]] = round(by_category.get(line["category"], 0) + line["amount"], 2)
    total_spend = round(sum(l["amount"] for l in spend), 2)
    total_inflow = round(sum(l["amount"] for l in income), 2)
    salary_inflow = round(sum(l["amount"] for l in income if l["kind"] == "salary"), 2)
    refunds = [{"date": d, "merchant": m, "amount": a} for (d, m, a) in REFUNDS.get(key, [])]
    refund_total = round(sum(r["amount"] for r in refunds), 2)
    merchant_totals = {}
    for line in spend:
        merchant_totals[line["merchant"]] = round(merchant_totals.get(line["merchant"], 0) + line["amount"], 2)
    top_merchants = [{"merchant": m, "amount": a}
                     for m, a in sorted(merchant_totals.items(), key=lambda kv: -kv[1])[:10]]
    return {
        "month": key,
        "start": f"{key}-01",
        "end": f"{key}-{last_day:02d}",
        "n_transactions": len(spend) + len(income),
        "total_spend": total_spend,
        "total_inflow": total_inflow,
        "salary_inflow": salary_inflow,
        "net_spend": round(total_spend - total_inflow, 2),
        "refund_total": refund_total,
        "by_category": by_category,
        "spend_lines": spend,
        "income_lines": income,
        "refunds_credits": refunds,
        "top_merchants": top_merchants,
        "anomalies": [{"date": d, "merchant": m, "amount": a, "why": w}
                      for (d, m, a, w) in ANOMALIES.get(key, [])],
        "excluded": [{"date": d, "merchant": m, "amount": a, "reason": r}
                     for (d, m, a, r) in EXCLUDED.get(key, [])],
    }


def main():
    sample = {
        "2026-07": build_month("2026-07", 2026, 7, 31),
        "2026-08": build_month("2026-08", 2026, 8, 31),
        "2026-09": build_month("2026-09", 2026, 9, 30),
    }
    js = "window.MONTH_DATA = " + json.dumps(sample, separators=(",", ":")) + ";"
    blob = base64.b64encode(js.encode("utf-8")).decode("ascii")

    html = SRC.read_text()
    pattern = r'<script src="data:application/javascript;base64,[A-Za-z0-9+/=]+">'
    html2, n = re.subn(pattern,
                       '<script src="data:application/javascript;base64,' + blob + '">',
                       html, count=1)
    assert n == 1, "data-uri script not found"

    # Copy patches for the sample build
    patches = [
        ("<title>Monthly Spending</title>",
         "<title>SideFi — Monthly Spending</title>"),
        ('"2024": "Oct–Dec · 3 months",\n        "2025": "Full year · 12 months",\n        "2026": "Jan–Sep · 9 months"',
         '"2026": "Jul–Sep · 3 months · sample data"'),
        ('"Snapshot through Sep 29, 2026 · Full 24-month history"',
         '"Snapshot through Sep 30, 2026 · Sample data"'),
        ("Oct 2024–Sep 2026 · USD",
         "Jul–Sep 2026 · Sample data · USD"),
        ('"Oct 2024–Sep 2026 · 24 months"',
         '"Jul–Sep 2026 · 3 months · sample data"'),
        ('"Two years, one clearer spending story."',
         '"Three sample months, one clearer spending story."'),
        # Hardcoded takeaways tied to real data (two functions) -> remove the
        # statements entirely so no real-data copy ships, even as dead code.
        ('if (month.month === "2026-09") return "Rent reshaped September.";\n        ', ''),
        ('if (month.month === "2026-08") return "Travel and taxes drove August.";\n        ', ''),
        ('const second = categories[1];\n        if (month.month === "2026-09") return "Rent remains the largest fixed cost. The Little Speed Shop is September\u2019s biggest discretionary charge, lifting services into the second-largest bucket.";\n        ',
         'const second = categories[1];\n        '),
        (';\n        if (month.month === "2026-08") return "The Airbnb stay and hotels, plus a $5,000 IRS payment, drove a travel-heavy August.";',
         ';'),
        # static fallbacks in the HTML shell
        ('<h1 id="headline">Rent reshaped September.</h1>',
         '<h1 id="headline">Three sample months.</h1>'),
        ('<p class="period-label" id="periodLabel">Through Sep 29</p>',
         '<p class="period-label" id="periodLabel">Sample data</p>'),
        # institution list + stale "Through Sep 29" in the dynamic period label
        ('(latest ? "Through Sep 29" : monthName.format(date)) + " \u00b7 Chase + Amex + SoFi + BofA/Merrill + Gemini"',
         '(latest ? "Through Sep 30, 2026" : monthName.format(date)) + " \u00b7 Sample data"'),
        # merchant prettifier learned real merchants -> sample entries
        ('"BILT PAYMENT": "Bilt (rent)",\n          "Lg Electronics USA": "LG Electronics",\n          "AMEX HOTEL COLLECTN AmexTravel.com": "Amex Travel hotel",\n          "AMEX Fine Hotels andAmexTravel.com": "Amex Fine Hotels + Resorts",\n          "CL *Chase Travel": "Chase Travel"',
         '"SAMPLE PROPERTY MGMT RENT": "Sample Property Mgmt (rent)",\n          "MTA*MTA": "Metro Transit"'),
        ('if (name.startsWith("ONLINE DOMESTIC WIRE TRANSFER")) return "Cayenne Realty Group";\n        if (name.startsWith("CHECK #") && name.includes("USCIS")) return "USCIS";\n        return name;',
         'return name;'),
        # lender annotation tied to real data
        ('(label === "Car loan" ? \' <span class="panel-note">\u00b7 Toyota Financial</span>\' : \'\')',
         "''"),
        # trend-chart annotations reference real months/amounts (would crash
        # year view on sample data via findIndex -> -1) -> empty set
        ('annotations = [\n          { id: "2025-04", label: "$25,080", dx: 0, dy: -20, anchor: "middle" },\n          { id: "2026-04", label: "$45,797", dx: -6, dy: -16, anchor: "end" },\n          { id: "2026-05", label: "$28,848", dx: 9, dy: -15, anchor: "start" },\n          { id: "2026-08", label: "$26,756", dx: -8, dy: -17, anchor: "end" }\n        ];',
         'annotations = [];'),
        # peak-month id set references real months -> empty for the sample
        ('const peakIds = new Set(["2025-04", "2026-04", "2026-05", "2026-08"]);',
         'const peakIds = new Set([]);'),
        # SVG accessibility copy tied to the real 24-month range -> generic
        ('<title id="trendTitle">Monthly net spending from October 2024 through September 2026</title>',
         '<title id="trendTitle">Monthly net spending, three sample months</title>'),
        ('<desc id="trendDesc">A line chart with peaks in April 2025, April 2026, May 2026, and August 2026. April 2026 is the highest month at $45,797.</desc>',
         '<desc id="trendDesc">A line chart of sample net spending over three months.</desc>'),
    ]
    for old, new in patches:
        assert old in html2, f"patch target missing: {old[:60]!r}"
        html2 = html2.replace(old, new, 1)

    # Year takeaways are hardcoded real-data narratives -> swap for sample copy
    sec_start = html2.find('<section class="panel takeaways-panel"')
    sec_end = html2.find('</section>', sec_start) + len('</section>')
    assert sec_start > 0 and sec_end > sec_start
    sample_takeaways = ('<section class="panel takeaways-panel" aria-label="Year takeaways">'
        '<article class="year-takeaway">'
        '<p class="takeaway-year">2026</p><h2>Rent leads</h2>'
        '<p>Housing is the largest fixed cost in the sample at $2,400 per month, followed by food and drink.</p>'
        '</article>'
        '<article class="year-takeaway">'
        '<p class="takeaway-year">Sample</p><h2>One-off spike</h2>'
        '<p>September includes a $899 appliance purchase, the sample\u2019s biggest discretionary charge.</p>'
        '</article>'
        '<article class="year-takeaway">'
        '<p class="takeaway-year">Sample</p><h2>Income vs spend</h2>'
        '<p>Payroll lands twice a month; net spend stays well under inflow across all three sample months.</p>'
        '</article></section>')
    html2 = html2[:sec_start] + sample_takeaways + html2[sec_end:]

    # Sanity: no real-data fingerprints in the sample data blob itself.
    # (cleanMerchant's display-name map in the app code may still name real
    # merchants it has learned; that is code, not transaction data.)
    sample_js = base64.b64decode(blob).decode("utf-8")
    for fingerprint in ["BILT PAYMENT", "The Little Speed Shop", "NY PRESBYTERIAN",
                        "NEXT BEAUTY", "2024-10", "2025-01"]:
        assert fingerprint not in sample_js, f"real data leak: {fingerprint}"

    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(html2)
    print("wrote", DST, len(html2), "bytes,", n, "data-uri replaced")


if __name__ == "__main__":
    main()

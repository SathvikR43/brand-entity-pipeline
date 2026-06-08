from database.db import get_connection
from datetime import datetime

def run_quality_checks():
    conn = get_connection()
    cur = conn.cursor()
    issues = []

    # Check 1: Missing country
    cur.execute("SELECT COUNT(*) FROM brands WHERE country = '' OR country IS NULL")
    missing_country = cur.fetchone()[0]
    if missing_country > 0:
        issues.append(f"⚠️  {missing_country} brands missing country")

    # Check 2: Missing industry
    cur.execute("SELECT COUNT(*) FROM brands WHERE industry = '' OR industry IS NULL")
    missing_industry = cur.fetchone()[0]
    if missing_industry > 0:
        issues.append(f"⚠️  {missing_industry} brands missing industry")

    # Check 3: Missing website
    cur.execute("SELECT COUNT(*) FROM brands WHERE website = '' OR website IS NULL")
    missing_website = cur.fetchone()[0]
    if missing_website > 0:
        issues.append(f"⚠️  {missing_website} brands missing website")

    # Check 4: Low confidence scores
    cur.execute("SELECT COUNT(*) FROM brands WHERE confidence_score < 0.8")
    low_confidence = cur.fetchone()[0]
    if low_confidence > 0:
        issues.append(f"⚠️  {low_confidence} brands with low confidence score (<0.8)")

    # Check 5: Total records
    cur.execute("SELECT COUNT(*) FROM brands")
    total = cur.fetchone()[0]

    # Log pipeline run
    cur.execute("""
        INSERT INTO pipeline_runs (run_at, records_ingested, records_resolved, status)
        VALUES (%s, %s, %s, %s)
    """, (datetime.now(), total, total, "completed" if not issues else "completed_with_warnings"))

    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ Quality check complete — {total} total brands in database")
    if issues:
        for issue in issues:
            print(issue)
    else:
        print("✅ No quality issues found")

    return issues

if __name__ == "__main__":
    run_quality_checks()
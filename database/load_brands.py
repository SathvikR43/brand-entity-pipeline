from database.db import get_connection

def load_brands(brands):
    conn = get_connection()
    cur = conn.cursor()
    inserted = 0

    for brand in brands:
        try:
            cur.execute("""
                INSERT INTO brands (name, canonical_name, country, industry, website, source, confidence_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (
                brand["name"],
                brand["name"],
                brand.get("country", ""),
                brand.get("industry", ""),
                brand.get("website", ""),
                brand.get("source", "wikidata"),
                1.0
            ))
            inserted += 1
        except Exception as e:
            print(f"❌ Error inserting {brand['name']}: {e}")
            conn.rollback()
            continue

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Loaded {inserted} brands into the database")

if __name__ == "__main__":
    from ingestion.fetch_brands import fetch_brands_from_wikidata
    brands = fetch_brands_from_wikidata()
    load_brands(brands)
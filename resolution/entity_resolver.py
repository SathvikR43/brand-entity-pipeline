from fuzzywuzzy import fuzz
from database.db import get_connection

def get_all_brands():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, canonical_name FROM brands")
    brands = cur.fetchall()
    cur.close()
    conn.close()
    return brands

def find_duplicates(threshold=85):
    brands = get_all_brands()
    duplicates = []

    for i in range(len(brands)):
        for j in range(i + 1, len(brands)):
            id1, name1, canonical1 = brands[i]
            id2, name2, canonical2 = brands[j]

            score = fuzz.token_sort_ratio(name1.lower(), name2.lower())

            if score >= threshold:
                duplicates.append({
                    "id1": id1,
                    "name1": name1,
                    "id2": id2,
                    "name2": name2,
                    "similarity_score": score
                })

    return duplicates

def resolve_duplicates(duplicates):
    conn = get_connection()
    cur = conn.cursor()
    resolved = 0

    for dup in duplicates:
        try:
            # Insert the duplicate as an alias of the first entity
            cur.execute("""
                INSERT INTO brand_aliases (brand_id, alias)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (dup["id1"], dup["name2"]))

            # Update confidence score on the canonical brand
            cur.execute("""
                UPDATE brands SET confidence_score = %s, updated_at = NOW()
                WHERE id = %s
            """, (round(dup["similarity_score"] / 100, 2), dup["id1"]))

            resolved += 1
        except Exception as e:
            print(f"❌ Error resolving {dup['name1']} / {dup['name2']}: {e}")
            conn.rollback()
            continue

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Resolved {resolved} duplicate entities")

if __name__ == "__main__":
    print("🔍 Finding duplicates...")
    duplicates = find_duplicates(threshold=85)
    print(f"Found {len(duplicates)} potential duplicates")
    for d in duplicates[:5]:
        print(f"  {d['name1']} <-> {d['name2']} (score: {d['similarity_score']})")
    resolve_duplicates(duplicates)
from ingestion.fetch_brands import fetch_brands_from_wikidata
from database.load_brands import load_brands
from resolution.entity_resolver import find_duplicates, resolve_duplicates
from quality.data_quality import run_quality_checks

def run():
    print("=" * 50)
    print("🚀 Brand Entity Pipeline Starting...")
    print("=" * 50)

    print("\n📥 Step 1: Ingesting brands from Wikidata...")
    brands = fetch_brands_from_wikidata()

    print("\n💾 Step 2: Loading brands into PostgreSQL...")
    load_brands(brands)

    print("\n🔍 Step 3: Running entity resolution...")
    duplicates = find_duplicates(threshold=85)
    print(f"   Found {len(duplicates)} potential duplicates")
    resolve_duplicates(duplicates)

    print("\n✅ Step 4: Running data quality checks...")
    run_quality_checks()

    print("\n" + "=" * 50)
    print("✅ Pipeline complete! API is ready at http://127.0.0.1:5000")
    print("=" * 50)

if __name__ == "__main__":
    run()
import requests
import json

def fetch_brands_from_wikidata():
    url = "https://query.wikidata.org/sparql"
    
    query = """
    SELECT ?company ?companyLabel ?countryLabel ?industryLabel ?website WHERE {
      ?company wdt:P31 wd:Q4830453.
      ?company wdt:P17 ?country.
      OPTIONAL { ?company wdt:P452 ?industry. }
      OPTIONAL { ?company wdt:P856 ?website. }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    LIMIT 100
    """
    
    headers = {
        "Accept": "application/json",
        "User-Agent": "BrandEntityPipeline/1.0"
    }
    
    params = {"query": query, "format": "json"}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        brands = []
        for item in data["results"]["bindings"]:
            brand = {
                "name": item.get("companyLabel", {}).get("value", ""),
                "country": item.get("countryLabel", {}).get("value", ""),
                "industry": item.get("industryLabel", {}).get("value", ""),
                "website": item.get("website", {}).get("value", ""),
                "source": "wikidata"
            }
            if brand["name"]:
                brands.append(brand)
        
        print(f"✅ Fetched {len(brands)} brands from Wikidata")
        return brands
    
    except Exception as e:
        print(f"❌ Failed to fetch brands: {e}")
        return []

if __name__ == "__main__":
    brands = fetch_brands_from_wikidata()
    print(json.dumps(brands[:3], indent=2))
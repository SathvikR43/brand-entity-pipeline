from flask import Flask, jsonify, request
from database.db import get_connection

app = Flask(__name__)

@app.route("/brands", methods=["GET"])
def get_brands():
    conn = get_connection()
    cur = conn.cursor()

    name = request.args.get("name")

    if name:
        cur.execute("""
            SELECT b.id, b.name, b.canonical_name, b.country, b.industry, 
                   b.website, b.source, b.confidence_score, b.updated_at
            FROM brands b
            WHERE LOWER(b.name) LIKE LOWER(%s)
        """, (f"%{name}%",))
    else:
        cur.execute("""
            SELECT b.id, b.name, b.canonical_name, b.country, b.industry,
                   b.website, b.source, b.confidence_score, b.updated_at
            FROM brands b
            ORDER BY b.confidence_score DESC
            LIMIT 50
        """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    brands = []
    for row in rows:
        brands.append({
            "id": row[0],
            "name": row[1],
            "canonical_name": row[2],
            "country": row[3],
            "industry": row[4],
            "website": row[5],
            "source": row[6],
            "confidence_score": row[7],
            "updated_at": str(row[8])
        })

    return jsonify({"count": len(brands), "brands": brands})

@app.route("/brands/<int:brand_id>/aliases", methods=["GET"])
def get_aliases(brand_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT a.alias, b.name as canonical_name
        FROM brand_aliases a
        JOIN brands b ON a.brand_id = b.id
        WHERE a.brand_id = %s
    """, (brand_id,))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    aliases = [{"alias": row[0], "canonical_name": row[1]} for row in rows]
    return jsonify({"brand_id": brand_id, "aliases": aliases})

@app.route("/quality", methods=["GET"])
def get_quality():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM pipeline_runs ORDER BY run_at DESC LIMIT 5")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    runs = []
    for row in rows:
        runs.append({
            "id": row[0],
            "run_at": str(row[1]),
            "records_ingested": row[2],
            "records_resolved": row[3],
            "status": row[4]
        })

    return jsonify({"pipeline_runs": runs})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
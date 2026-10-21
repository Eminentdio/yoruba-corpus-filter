import csv
from collections import Counter
from src.tokeniser import create_yoruba_pipeline
from src.particle_ruler import register_particle_rules
from src.quality_filter import YorubaCorpusFilter

def main():
    print("--- INITIALISING YORÙBÁ LIGHTWEIGHT NLP PIPELINE ---")
    
    # 1. Instantiate the rule-based blank pipeline
    nlp = create_yoruba_pipeline()
    nlp = register_particle_rules(nlp)
    
    filter_engine = YorubaCorpusFilter(nlp)
    
    # 2. Ingest Raw Dataset
    input_path = "data/raw/yor_sample_web.csv"
    with open(input_path, newline="", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    print(f"Loaded {len(rows)} rows from {input_path}\n")

    # 3. Run Pipeline
    audited_rows = []
    for row in rows:
        result = filter_engine.audit_sentence(row["text"])
        audited_rows.append({
            **row,
            "clean_text": result["text"],
            "is_valid": result["is_valid"],
            "audit_reason": result["reason"],
        })

    # 4. Split and Export
    clean_rows = [row for row in audited_rows if row["is_valid"]]
    rejected_rows = [row for row in audited_rows if not row["is_valid"]]
    clean_fields = [
        name for name in dict.fromkeys([*fieldnames, "clean_text", "is_valid", "audit_reason"])
        if name not in {"is_valid", "audit_reason"}
    ]
    report_fields = list(dict.fromkeys([*fieldnames, "clean_text", "is_valid", "audit_reason"]))

    with open("data/processed/clean_corpus.csv", "w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=clean_fields)
        writer.writeheader()
        writer.writerows(clean_rows)
    with open("data/processed/rejected_report.csv", "w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=report_fields)
        writer.writeheader()
        writer.writerows(rejected_rows)

    # 5. Output Summary
    print("--- CORPUS AUDIT REPORT ---")
    print(f"Valid sentences passed : {len(clean_rows)}")
    print(f"Defective rows dropped : {len(rejected_rows)}\n")
    print("Rejection Breakdown:")
    print("\n".join(
        f"{reason}    {count}"
        for reason, count in Counter(row["audit_reason"] for row in rejected_rows).most_common()
    ))

if __name__ == "__main__":
    main()
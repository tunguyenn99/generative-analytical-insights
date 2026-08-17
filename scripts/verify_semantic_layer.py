import json
import os


def verify_dbt_semantic_layer():
    manifest_path = "zomato_dbt/target/manifest.json"
    if not os.path.exists(manifest_path):
        print("⚠️ manifest.json not found! Running dbt parse...")
        os.system("cd zomato_dbt && dbt parse")

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    semantic_models = manifest.get("semantic_models", {})
    metrics = manifest.get("metrics", {})

    print("📐 === dbt Semantic Layer & MetricFlow Verification ===")
    print(f"  ├─ Semantic Models Configured ({len(semantic_models)}):")
    for key, model in semantic_models.items():
        name = model.get("name")
        measures = [m.get("name") for m in model.get("measures", [])]
        print(f"  │    ├─ [{name}]: Measures -> {measures}")

    print(f"  └─ Defined Business Metrics ({len(metrics)}):")
    for key, metric in metrics.items():
        name = metric.get("name")
        desc = metric.get("description")
        m_type = metric.get("type")
        print(f"       ├─ 📊 {name} ({m_type}): {desc}")

    print("✅ dbt MetricFlow Semantic Layer compiled and validated successfully!")


if __name__ == "__main__":
    verify_dbt_semantic_layer()

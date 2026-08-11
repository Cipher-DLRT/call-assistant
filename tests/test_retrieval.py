import hashlib
import json

import pytest

from app.loop.retrieval import PackError, load_pack


def write_pack(tmp_path):
    rows = [
        {
            "id": "pricing",
            "fact_text": "Enterprise pricing includes volume discounts",
            "structured_value": {"minimum_seats": 100},
            "tier": "company",
            "volatility_class": "medium",
            "shareability": "public",
            "verified_at": "2026-08-01",
        },
        {
            "id": "security",
            "fact_text": "Customer data is encrypted at rest",
            "structured_value": {"cipher": "AES 256"},
            "tier": "company",
            "volatility_class": "low",
            "shareability": "public",
            "verified_at": "2026-08-02",
        },
        {
            "id": "deployment",
            "fact_text": "Private cloud deployment is supported",
            "structured_value": {"regions": ["Dubai", "Frankfurt"]},
            "tier": "product",
            "volatility_class": "medium",
            "shareability": "public",
            "verified_at": "2026-08-03",
        },
        {
            "id": "support",
            "fact_text": "Premium support operates around the clock",
            "structured_value": {"response_minutes": 30},
            "tier": "service",
            "volatility_class": "medium",
            "shareability": "locked",
            "verified_at": "2026-08-04",
        },
        {
            "id": "integration",
            "fact_text": "The platform connects to business applications",
            "structured_value": {"connectors": {"salesforce": True, "sap": True}},
            "tier": "product",
            "volatility_class": "low",
            "shareability": "public",
            "verified_at": "2026-08-05",
        },
    ]
    pack_path = tmp_path / "canon.json"
    pack_path.write_text(json.dumps(rows))
    manifest = {
        "exported_at": "2026-08-11T00:00:00Z",
        "active_count": len(rows),
        "total_count": len(rows) + 2,
        "sha256": hashlib.sha256(pack_path.read_bytes()).hexdigest(),
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest))
    return pack_path, manifest_path, manifest


def test_search_ranks_match_respects_top_k_and_omits_zero_scores(tmp_path):
    pack_path, manifest_path, _ = write_pack(tmp_path)
    pack = load_pack(pack_path, manifest_path)

    results = pack.search("Do you offer AES encryption and Salesforce?", top_k=1)

    assert len(results) == 1
    assert results[0]["id"] == "security"
    assert set(results[0]) == {"id", "fact_text", "shareability", "verified_at", "score"}
    assert pack.search("unmentionedword") == []


def test_sha_mismatch_raises(tmp_path):
    pack_path, manifest_path, manifest = write_pack(tmp_path)
    manifest["sha256"] = "0" * 64
    manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(PackError):
        load_pack(pack_path, manifest_path)


def test_count_mismatch_raises(tmp_path):
    pack_path, manifest_path, manifest = write_pack(tmp_path)
    manifest["active_count"] += 1
    manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(PackError):
        load_pack(pack_path, manifest_path)


def test_active_equal_total_raises(tmp_path):
    pack_path, manifest_path, manifest = write_pack(tmp_path)
    manifest["total_count"] = manifest["active_count"]
    manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(PackError):
        load_pack(pack_path, manifest_path)


def test_missing_manifest_raises(tmp_path):
    pack_path, manifest_path, _ = write_pack(tmp_path)
    manifest_path.unlink()
    with pytest.raises(PackError):
        load_pack(pack_path, manifest_path)

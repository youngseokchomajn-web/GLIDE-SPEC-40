import os
import pytest

def test_orc_operation_protocol_exists_and_covers_contract():
    doc_path = "docs/ORC_OPERATION_PROTOCOL.md"
    assert os.path.exists(doc_path), "docs/ORC_OPERATION_PROTOCOL.md must exist."
    
    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    required_phrases = [
        "orc 작동",
        "Repository State > Conversation Claim",
        "STEP 1",
        "STEP 2",
        "STEP 3",
        "Dataset Identity",
        "Baseline Integrity",
        "Information Leakage",
        "Benchmark Overfitting",
        "Cross-Domain Stability",
        "Manufacturing Relevance",
        "Physical Validation",
        "NON_ESTIMABLE",
        "BLIND SCORING IS NOT AUTHORIZED",
        "APPROVE",
        "REJECT",
        "DATA_REQUIRED",
        "EXPERIMENT",
        "FIX_REQUIRED",
        "No-Op Rule",
        "max_consecutive_fix_attempts",
        "Rev.8.1",
        "Rev.7.3",
        "Rule 16",
    ]
    
    for phrase in required_phrases:
        assert phrase.lower() in content.lower(), f"Missing required protocol element: {phrase}"

def test_protocol_cross_reference():
    protocol_path = ".agent/PROTOCOL.md"
    with open(protocol_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "ORC_OPERATION_PROTOCOL.md" in content, "PROTOCOL.md must reference ORC_OPERATION_PROTOCOL.md."

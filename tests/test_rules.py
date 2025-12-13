from pathlib import Path
import sys

# Ensure project root (where parser.py and rules.py live) is on sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from parser import parse_provisioner_yaml
from rules import run_analysis, generate_summary


FIXTURES = Path(__file__).parent / "fixtures"


def _read_fixture(name: str) -> str:
    path = FIXTURES / name
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_rules_basic_file_counts_match_summary():
    """
    Sanity test on a 'normal' config:

    - Parser returns the expected number of provisioners / nodeclasses
    - Severity counts in the summary match the actual Issue list
    - Health score is within [0, health_score_max]
    """
    yaml_content = _read_fixture("basic-karpenter.yaml")
    provisioners, nodeclasses = parse_provisioner_yaml(yaml_content)

    issues = run_analysis(provisioners, nodeclasses)
    summary = generate_summary(provisioners, issues, nodeclasses)

    # Basic shape
    assert summary["optimization_status"]["total_provisioners"] == len(provisioners)
    assert summary["ec2_nodeclass_count"] == len(nodeclasses)

    # Severity counts should match exactly
    computed = {"high": 0, "medium": 0, "low": 0}
    for issue in issues:
        sev = (issue.severity or "").lower()
        if sev in computed:
            computed[sev] += 1

    assert summary["issues_by_severity"] == computed

    # Health score within valid range
    assert 0 <= summary["health_score"] <= summary["health_score_max"]


def test_rules_edge_cases_health_and_ttl_classification():
    """
    Edge-case config to exercise TTL rules and scoring:

    - A provisioner with TTL=7200s must show up as a LOW severity TTL issue.
    - A provisioner with no TTL configured must show up as a MEDIUM severity TTL issue.
    - Health score should be non-trivial (strictly between 0 and max) when issues exist.
    """
    yaml_content = _read_fixture("edge-cases-karpenter.yaml")
    provisioners, nodeclasses = parse_provisioner_yaml(yaml_content)

    issues = run_analysis(provisioners, nodeclasses)
    summary = generate_summary(provisioners, issues, nodeclasses)

    # 1) Make sure the weird TTL=7200s is classified as LOW severity
    low_issue_msgs = [i.message for i in issues if i.severity == "low"]
    found_weird_ttl = any(
        "7200" in msg or "np-weird-ttl" in msg for msg in low_issue_msgs
    )
    assert found_weird_ttl, "Expected np-weird-ttl TTL=7200s to be flagged as low severity"

    # 2) Make sure at least one 'missing TTL' shows up as MEDIUM
    medium_ttl_issues = [
        i
        for i in issues
        if i.severity == "medium"
        and "ttlSecondsAfterEmpty (or equivalent) is not configured" in i.message
    ]
    assert medium_ttl_issues, "Expected at least one medium-severity issue for missing TTL"

    # 3) Health score should not collapse to 0 when there are issues
    total_issues = (
        summary["issues_by_severity"]["high"]
        + summary["issues_by_severity"]["medium"]
        + summary["issues_by_severity"]["low"]
    )
    assert total_issues > 0
    assert 0 < summary["health_score"] < summary["health_score_max"]
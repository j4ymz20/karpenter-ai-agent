import os
import sys
from pathlib import Path

# Ensure project root is on sys.path so "import parser" etc. work
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from parser import parse_provisioner_yaml  # type: ignore
from models import ProvisionerConfig, EC2NodeClassConfig  # type: ignore


FIXTURES = Path(__file__).parent / "fixtures"


def _read_fixture(name: str) -> str:
    path = FIXTURES / name
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_parse_basic_karpenter_yaml():
    yaml_content = _read_fixture("basic-karpenter.yaml")

    provisioners, nodeclasses = parse_provisioner_yaml(yaml_content)

    # We at least get *something* back
    assert len(provisioners) > 0

    # Types are correct
    assert all(isinstance(p, ProvisionerConfig) for p in provisioners)
    assert all(isinstance(nc, EC2NodeClassConfig) for nc in nodeclasses)

    # Basic sanity checks on known names (adjust if your names differ)
    names = {p.name for p in provisioners}
    assert "default-provisioner" in names
    assert "perf-nodepool" in names


def test_parse_edge_case_yaml():
    yaml_content = _read_fixture("edge-cases-karpenter.yaml")

    provisioners, nodeclasses = parse_provisioner_yaml(yaml_content)

    # Edge file should have multiple provisioners and at least one EC2NodeClass
    assert len(provisioners) >= 3
    assert len(nodeclasses) >= 1

    # Check that at least one NodePool with nodeClass reference is recognized
    np_names = {p.name for p in provisioners}
    assert "np-string-nodeclass" in np_names or "np-dict-nodeclass" in np_names
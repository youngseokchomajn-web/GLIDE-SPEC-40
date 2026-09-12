"""
GLIDE-SPEC 40 - Automated Tests for Layer 1 Virtual Mechanistic Simulator
Verifies prior estimations, Monte Carlo bounds, and strict firewall flags.
"""

from pathlib import Path
import pytest
import numpy as np

from src.modeling.virtual_simulator import VirtualMechanisticSimulator, VirtualSimulationResult


@pytest.fixture
def simulator():
    return VirtualMechanisticSimulator()


@pytest.fixture
def domain_priors_dir():
    return Path(__file__).resolve().parent.parent / "benchmarks" / "domain_priors"


def test_domain_prior_files_exist(domain_priors_dir):
    fric_csv = domain_priors_dir / "imperial_friction" / "wax_oil_friction_data.csv"
    stick_csv = domain_priors_dir / "lipstick_17pct_anchor" / "lipstick_17pct_wax_benchmark.csv"
    wax_csv = domain_priors_dir / "tuberlin_wax_variability" / "natural_wax_batch_variability_summary.csv"

    assert fric_csv.exists(), "Imperial friction CSV must exist"
    assert stick_csv.exists(), "Lipstick 17% anchor CSV must exist"
    assert wax_csv.exists(), "TU Berlin wax variability CSV must exist"


def test_virtual_simulator_center_point_priors(simulator):
    # Test center point: SynWax 12%, CanWax 5%, Dimethicone 17%, Caprylyl 11%, Fill 80C
    priors = simulator.estimate_point_priors(
        syn_wax_pct=12.0,
        candelilla_wax_pct=5.0,
        dimethicone_pct=17.0,
        caprylyl_pct=11.0,
        fill_temp_c=80.0
    )

    # Drop point should be very close to Rev.7.3 target (61.5°C)
    assert 60.0 <= priors["drop_point_c"] <= 63.0

    # Hardness should be within plausible cosmetic stick range
    assert 650.0 <= priors["hardness_gf"] <= 900.0

    # Transfer at 10°C should be around 0.04 to 0.06 g
    assert 0.035 <= priors["transfer_g_10c"] <= 0.065

    # Friction CoF should be low lubricious range
    assert 0.10 <= priors["friction_cof"] <= 0.20


def test_virtual_simulator_monte_carlo_distribution(simulator):
    result = simulator.simulate(
        syn_wax_pct=12.0,
        candelilla_wax_pct=5.0,
        dimethicone_pct=17.0,
        caprylyl_pct=11.0,
        fill_temp_c=80.0,
        n_monte_carlo=500,
        random_seed=123
    )

    assert isinstance(result, VirtualSimulationResult)
    # STRICT FIREWALL CHECK
    assert result.data_origin == "VIRTUAL_DOMAIN_PRIOR"
    assert result.is_empirical_gs40 is False
    assert "PRE-PILOT ESTIMATE" in result.warning_notice

    # Check distribution statistics
    assert result.predicted_hardness_gf.p05 < result.predicted_hardness_gf.mean < result.predicted_hardness_gf.p95
    assert result.predicted_transfer_g_10c.p05 < result.predicted_transfer_g_10c.mean < result.predicted_transfer_g_10c.p95
    assert result.predicted_drop_point_c.p05 < result.predicted_drop_point_c.mean < result.predicted_drop_point_c.p95
    assert result.predicted_friction_cof.p05 < result.predicted_friction_cof.mean < result.predicted_friction_cof.p95

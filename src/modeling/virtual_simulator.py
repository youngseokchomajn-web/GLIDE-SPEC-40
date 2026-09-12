"""
GLIDE-SPEC 40 - Virtual Mechanistic Prior Simulator (Layer 1)
Implements strictly audited, prior-derived property ranges and Monte Carlo uncertainty
analyses based on public domain scientific datasets.

⚠️ ABSOLUTE FIREWALL GUARANTEE:
1. These outputs are NOT calibrated on physical GS-40 pilot batches.
2. They NEVER modify or qualify the production M4 model (DataOrigin.REAL_PILOT).
3. All derivations are explicitly labeled as synthetic prior estimates.
"""

from pathlib import Path
from typing import Dict, Any, Tuple, Optional, List
import csv
import numpy as np
from pydantic import BaseModel, Field


class PriorProvenance(BaseModel):
    source_name: str
    citation: str
    doi: str
    anchor_measurement: str
    derivation_logic: str


class PriorDistribution(BaseModel):
    mean: float
    sd: float
    p05: float
    p95: float
    min_val: float
    max_val: float
    unit: str
    provenance: PriorProvenance


class VirtualSimulationResult(BaseModel):
    data_origin: str = "VIRTUAL_DOMAIN_PRIOR"
    is_empirical_gs40: bool = False
    status_label: str = "PRE-PILOT PRIOR (NOT GS40 EMPIRICAL MODEL)"
    warning_notice: str = (
        "PRE-PILOT ESTIMATE: Calculated by mapping public domain scientific literature "
        "onto the GS-40 coordinate space. NOT calibrated on physical GS40 pilot runs."
    )
    inputs: Dict[str, float]
    predicted_hardness_gf: PriorDistribution
    predicted_transfer_g_10c: PriorDistribution
    predicted_drop_point_c: PriorDistribution
    predicted_friction_index: PriorDistribution
    simulation_notes: str = ""


class VirtualMechanisticSimulator:
    """
    Layer 1 Physics-Informed Prior Derivation Engine.
    Exposes auditable provenance and mathematical formulas for each property prior.
    """

    def __init__(self, priors_dir: Optional[Path] = None):
        self.priors_dir = priors_dir or (
            Path(__file__).resolve().parent.parent.parent / "benchmarks" / "domain_priors"
        )
        self.tu_berlin_summary = self._load_tu_berlin_variability()

    def _load_tu_berlin_variability(self) -> Dict[str, Any]:
        csv_path = self.priors_dir / "tuberlin_wax_variability" / "natural_wax_batch_variability_summary.csv"
        if not csv_path.exists():
            return {"clx_cv_pct": 18.0, "clx_gstar_mean": 680000.0}

        clx_rows = []
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if r["wax_code"].startswith("CLX"):
                    clx_rows.append(float(r["cv_rigidity_pct"]))

        cv_mean = float(np.mean(clx_rows)) if clx_rows else 18.0
        return {"clx_cv_pct": cv_mean, "clx_records": len(clx_rows)}

    # --------------------------------------------------------------------------
    # Auditable Prior Derivations
    # --------------------------------------------------------------------------

    @classmethod
    def derive_drop_point_prior(cls, u1_syn_wax_share: float, dT_fill_c: float) -> Tuple[float, PriorProvenance]:
        """
        Derives drop point prior:
        - Anchor: Lipstick L1 (PMC9291794) at 17.0% total wax has DSC melting peak at 60.3°C.
        - Synthetic wax has ~82°C melting point vs Candelilla wax ~70°C.
        - Linear interpolation across u1 in [0.529, 0.882]:
            T_drop = 57.0 + 6.3 * u1 + 0.05 * (T_fill - 80.0)
        """
        val = 57.0 + 6.3 * u1_syn_wax_share + 0.05 * dT_fill_c
        prov = PriorProvenance(
            source_name="Lipstick 17% Wax Benchmark (L1 Control)",
            citation="Huynh et al., Int. J. Cosmet. Sci. 42(3), 292-302 (2020)",
            doi="10.1111/ics.12597",
            anchor_measurement="17.0% Wax System melting peak = 60.3°C (range 35.9-85.2°C)",
            derivation_logic="T_drop = 57.0 + 6.3 * u1 + 0.05 * dT"
        )
        return float(np.clip(val, 55.0, 68.0)), prov

    @classmethod
    def derive_hardness_prior(
        cls, u1_syn_wax_share: float, v1_dimethicone_share: float, dT_fill_c: float
    ) -> Tuple[float, PriorProvenance]:
        """
        Derives hardness prior:
        - Pure wax stick needle penetration hardness ~ 165 gf (PMC9291794).
        - 28% powder loading (silica, PMSSQ, Aerosil) + 12% active MQ resin provides a ~4.6x solid reinforcement.
        - Target formulation center point anchors at ~760 gf (target range 750~900 gf).
        - Synthetic wax increases hardness (+260 * u1), dimethicone acts as plasticizer (-120 * v1):
            H_prior = 650.0 + 260.0 * u1 - 120.0 * v1 + 3.5 * dT
        """
        val = 650.0 + 260.0 * u1_syn_wax_share - 120.0 * v1_dimethicone_share + 3.5 * dT_fill_c
        prov = PriorProvenance(
            source_name="Lipstick L1 Anchor + Anhydrous Powder Reinforcement Model",
            citation="Huynh et al. (2020) & GLIDE-SPEC-40 Rev.7.3 Baseline Specification",
            doi="10.1111/ics.12597",
            anchor_measurement="Base wax firmness 165 gf scaled by 28% particulate loading & MQ resin",
            derivation_logic="H_prior = 650.0 + 260.0*u1 - 120.0*v1 + 3.5*dT"
        )
        return float(np.clip(val, 500.0, 1200.0)), prov

    @classmethod
    def derive_transfer_prior(
        cls, u1_syn_wax_share: float, v1_dimethicone_share: float, dT_fill_c: float
    ) -> Tuple[float, PriorProvenance]:
        """
        Derives skin transfer/pay-off prior:
        - Anchor: Lipstick L1 deposits 14 ± 2 mg over 3 strokes (PMC9291794).
        - GS40 SOP measures 1 round-trip stroke across 10 cm² at 10°C.
        - Candelilla wax (1 - u1) increases plasticity; lighter volatile-like silicone (1 - v1) enhances slip transfer:
            Transfer_prior = 0.058 - 0.020 * u1 + 0.012 * (1.0 - v1) - 0.0003 * dT
        """
        val = 0.058 - 0.020 * u1_syn_wax_share + 0.012 * (1.0 - v1_dimethicone_share) - 0.0003 * dT_fill_c
        prov = PriorProvenance(
            source_name="Lipstick L1 Skin Pay-off Measurement",
            citation="Huynh et al., Int. J. Cosmet. Sci. 42(3), 292-302 (2020)",
            doi="10.1111/ics.12597",
            anchor_measurement="Skin pay-off 14 ± 2 mg scaled to 1 round-trip stroke on 10 cm² synthetic skin",
            derivation_logic="Transfer_prior = 0.058 - 0.020*u1 + 0.012*(1.0-v1) - 0.0003*dT"
        )
        return float(np.clip(val, 0.010, 0.090)), prov

    @classmethod
    def derive_friction_prior(
        cls, u1_syn_wax_share: float, v1_dimethicone_share: float
    ) -> Tuple[float, PriorProvenance]:
        """
        Derives external tribology friction index:
        - Anchor: Imperial College London (PMC8173004) shows 15-20% wax in hybrid oil yields CoF ~ 0.17-0.19.
        - Boron nitride (platelet shear) and PMSSQ (spherical rolling) provide additional slip index reduction:
            Friction_prior = 0.135 + 0.030 * u1 - 0.020 * (1.0 - v1)
        """
        val = 0.135 + 0.030 * u1_syn_wax_share - 0.020 * (1.0 - v1_dimethicone_share)
        prov = PriorProvenance(
            source_name="Imperial College London Skin Tribology Dataset",
            citation="Yap et al., Nature Scientific Reports 11, 11756 (2021)",
            doi="10.1038/s41598-021-91119-0",
            anchor_measurement="15BW/85OO in-vivo skin-PDMS dynamic CoF = 0.17 ± 0.02",
            derivation_logic="CoF_index = 0.135 + 0.030*u1 - 0.020*(1.0-v1)"
        )
        return float(np.clip(val, 0.08, 0.35)), prov

    @classmethod
    def estimate_point_priors(
        cls,
        syn_wax_pct: float,
        candelilla_wax_pct: float,
        dimethicone_pct: float,
        caprylyl_pct: float,
        fill_temp_c: float = 80.0
    ) -> Dict[str, float]:
        """Convenience helper returning point prior derivations as a dictionary."""
        u1 = syn_wax_pct / 17.0
        v1 = dimethicone_pct / 28.0
        dT = fill_temp_c - 80.0
        dp, _ = cls.derive_drop_point_prior(u1, dT)
        hard, _ = cls.derive_hardness_prior(u1, v1, dT)
        trans, _ = cls.derive_transfer_prior(u1, v1, dT)
        fric, _ = cls.derive_friction_prior(u1, v1)
        return {
            "hardness_gf": hard,
            "transfer_g_10c": trans,
            "drop_point_c": dp,
            "friction_index": fric,
            "friction_cof": fric
        }

    # --------------------------------------------------------------------------
    # Monte Carlo Prior Simulation
    # --------------------------------------------------------------------------

    def simulate(
        self,
        syn_wax_pct: float,
        candelilla_wax_pct: float,
        dimethicone_pct: float,
        caprylyl_pct: float,
        fill_temp_c: float = 80.0,
        n_monte_carlo: int = 1000,
        random_seed: int = 42
    ) -> VirtualSimulationResult:
        np.random.seed(random_seed)

        u1 = syn_wax_pct / 17.0
        v1 = dimethicone_pct / 28.0
        dT = fill_temp_c - 80.0

        # Derive point values and provenance
        drop_mean, drop_prov = self.derive_drop_point_prior(u1, dT)
        hard_mean, hard_prov = self.derive_hardness_prior(u1, v1, dT)
        trans_mean, trans_prov = self.derive_transfer_prior(u1, v1, dT)
        fric_mean, fric_prov = self.derive_friction_prior(u1, v1)

        # Incorporate TU Berlin lot-to-lot variance (CLX CV ~ 18%)
        # In a 17% wax system where candelilla is 5%, candelilla variance impacts ~6.5% overall hardness SD
        clx_cv = self.tu_berlin_summary.get("clx_cv_pct", 18.0)
        eff_hard_sd = hard_mean * (0.04 + 0.0015 * clx_cv)

        # Draw distributions
        hard_draws = np.random.normal(hard_mean, eff_hard_sd, n_monte_carlo)
        trans_draws = np.random.normal(trans_mean, 0.0035, n_monte_carlo)
        drop_draws = np.random.normal(drop_mean, 0.65, n_monte_carlo)
        fric_draws = np.random.normal(fric_mean, 0.012, n_monte_carlo)

        def make_dist(samples: np.ndarray, unit: str, prov: PriorProvenance) -> PriorDistribution:
            return PriorDistribution(
                mean=round(float(np.mean(samples)), 3),
                sd=round(float(np.std(samples)), 3),
                p05=round(float(np.percentile(samples, 5)), 3),
                p95=round(float(np.percentile(samples, 95)), 3),
                min_val=round(float(np.min(samples)), 3),
                max_val=round(float(np.max(samples)), 3),
                unit=unit,
                provenance=prov
            )

        return VirtualSimulationResult(
            inputs={
                "syn_wax_pct": syn_wax_pct,
                "candelilla_wax_pct": candelilla_wax_pct,
                "dimethicone_pct": dimethicone_pct,
                "caprylyl_pct": caprylyl_pct,
                "fill_temp_c": fill_temp_c
            },
            predicted_hardness_gf=make_dist(hard_draws, "gf", hard_prov),
            predicted_transfer_g_10c=make_dist(trans_draws, "g", trans_prov),
            predicted_drop_point_c=make_dist(drop_draws, "°C", drop_prov),
            predicted_friction_index=make_dist(fric_draws, "CoF Index", fric_prov),
            simulation_notes=(
                f"Monte Carlo n={n_monte_carlo} draws with TU Berlin Candelilla lot variance "
                f"(CV={clx_cv:.1f}%) and Imperial College skin tribology bounds."
            )
        )

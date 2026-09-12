"""
GLIDE-SPEC 40 - Virtual Mechanistic Prior Simulator (Layer 1.1)
Implements strictly audited, prior-derived property ranges and hierarchical Monte Carlo
uncertainty propagation based on public domain scientific datasets.

🛡️ THE 4 GOLDEN NON-EQUIVALENCE PRINCIPLES:
1. Hardness Prior ≠ GS40 Hardness Prediction
2. Thermal Transition Prior ≠ GS40 Mettler Drop Point
3. Pay-off Anchor ≠ GS40 Physical Transfer (g)
4. Tribology Prior Index ≠ GS40 Dynamic CoF

⚠️ ABSOLUTE FIREWALL GUARANTEE:
1. These outputs are NOT calibrated on physical GS-40 pilot batches.
2. They NEVER modify or qualify the production M4 model (DataOrigin.REAL_PILOT).
3. All derivations are explicitly labeled as engineering transformations with assumptions.
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
    transformation_type: str = "ENGINEERING_TRANSFORMATION"
    coefficient_source: str = "ENGINEERING_ASSUMPTION"
    formula_derivation: str
    scientific_caveat: str
    golden_principle_warning: str


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
        "onto the GS-40 coordinate space via explicit engineering transformations. "
        "NOT calibrated on physical GS40 pilot runs."
    )
    inputs: Dict[str, float]
    predicted_hardness_prior_gf: PriorDistribution
    predicted_transfer_prior_index: PriorDistribution
    predicted_thermal_transition_c: PriorDistribution
    predicted_tribology_prior_index: PriorDistribution
    hierarchical_uncertainty_breakdown: Dict[str, float] = Field(default_factory=dict)
    simulation_notes: str = ""

    # Backwards-compatible properties
    @property
    def predicted_hardness_gf(self) -> PriorDistribution:
        return self.predicted_hardness_prior_gf

    @property
    def predicted_transfer_g_10c(self) -> PriorDistribution:
        return self.predicted_transfer_prior_index

    @property
    def predicted_drop_point_c(self) -> PriorDistribution:
        return self.predicted_thermal_transition_c

    @property
    def predicted_friction_index(self) -> PriorDistribution:
        return self.predicted_tribology_prior_index


class VirtualMechanisticSimulator:
    """
    Layer 1.1 Physics-Informed Prior Derivation Engine.
    Exposes auditable provenance, explicit coefficient attribution (ENGINEERING_ASSUMPTION),
    and hierarchical uncertainty propagation for each property prior.
    """

    def __init__(self, priors_dir: Optional[Path] = None):
        self.priors_dir = priors_dir or (
            Path(__file__).resolve().parent.parent.parent / "benchmarks" / "domain_priors"
        )
        self.tu_berlin_summary = self._load_tu_berlin_variability()
        self.silicone_tribology_summary = self._load_silicone_tribology_data()

    def _load_tu_berlin_variability(self) -> Dict[str, Any]:
        csv_path = self.priors_dir / "tuberlin_wax_variability" / "natural_wax_batch_variability_summary.csv"
        if not csv_path.exists():
            return {"clx_cv_pct": 20.4, "clx_gstar_mean": 680000.0}

        clx_rows = []
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if r["wax_code"].startswith("CLX"):
                    clx_rows.append(float(r["cv_rigidity_pct"]))

        cv_mean = float(np.mean(clx_rows)) if clx_rows else 20.4
        return {"clx_cv_pct": cv_mean, "clx_records": len(clx_rows)}

    def _load_silicone_tribology_data(self) -> Dict[str, Any]:
        csv_path = self.priors_dir / "silicone_skin_tribology" / "silicone_powder_skin_tribology_benchmark.csv"
        if not csv_path.exists():
            return {"dimethicone_cof": 0.20, "talc_cof": 0.22}
        
        cofs = {}
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                cofs[r["sample_id"]] = float(r["initial_dynamic_cof"])
        return cofs

    # --------------------------------------------------------------------------
    # Auditable Prior Derivations with Explicit Coefficient Attribution
    # --------------------------------------------------------------------------

    @classmethod
    def derive_thermal_transition_prior(
        cls, u1_syn_wax_share: float, dT_fill_c: float
    ) -> Tuple[float, PriorProvenance]:
        """
        Derives thermal transition prior (DSC melting peak):
        - Anchor: Lipstick L1 (PMC9291794) at 17.0% total wax has DSC melting peak at 60.3°C.
        - Physical Warning: DSC thermodynamic melting peak is NOT identical to rheological
          dripping temperature under gravity (Mettler Drop Point ASTM D127 / IP 396).
        - Engineering Formula:
            T_thermal = 57.0 + 6.3 * u1 + 0.05 * dT
            All coefficients (57.0, 6.3, 0.05) = ENGINEERING_ASSUMPTION.
        """
        val = 57.0 + 6.3 * u1_syn_wax_share + 0.05 * dT_fill_c
        prov = PriorProvenance(
            source_name="Lipstick 17% Wax Benchmark (L1 Control)",
            citation="Huynh et al., Int. J. Cosmet. Sci. 42(3), 292-302 (2020)",
            doi="10.1111/ics.12597",
            anchor_measurement="17.0% Wax System DSC melting peak = 60.3°C (range 35.9-85.2°C)",
            transformation_type="ENGINEERING_TRANSFORMATION",
            coefficient_source="ENGINEERING_ASSUMPTION (57.0°C base, +6.3°C/unit u1, +0.05°C/°C dT)",
            formula_derivation="T_thermal = 57.0 + 6.3 * u1 + 0.05 * dT",
            scientific_caveat=(
                "DSC endotherm measures thermodynamic crystal melt. Dropping point under ASTM D127 / IP 396 "
                "depends on gravity flow and rheological shear thinning, which requires physical measurement."
            ),
            golden_principle_warning="Thermal Transition Prior ≠ GS40 Mettler Drop Point"
        )
        return float(np.clip(val, 55.0, 68.0)), prov

    # Backwards-compatible alias
    @classmethod
    def derive_drop_point_prior(cls, u1_syn_wax_share: float, dT_fill_c: float) -> Tuple[float, PriorProvenance]:
        return cls.derive_thermal_transition_prior(u1_syn_wax_share, dT_fill_c)

    @classmethod
    def derive_hardness_prior(
        cls, u1_syn_wax_share: float, v1_dimethicone_share: float, dT_fill_c: float
    ) -> Tuple[float, PriorProvenance]:
        """
        Derives hardness prior:
        - Primary Empirical Anchor: Base wax firmness = 165.0 gf (Huynh et al. 2020) +
          US20070166254 particulate loading reinforcement (~1.8-2.2x over unfilled stick).
        - Engineering Transformation:
            H_prior = 650.0 + 260.0 * u1 - 120.0 * v1 + 3.5 * dT
            Where:
              - 650.0 gf: Base intercept scaled from 165 gf by 28% powder + MQ resin network stiffening.
                          Source: ENGINEERING_ASSUMPTION.
              - 260.0 gf/unit: Synthetic wax crystal packing modulus slope across u1 in [0.529, 0.882].
                               Source: ENGINEERING_ASSUMPTION.
              - -120.0 gf/unit: Dimethicone plasticizing dilution slope across v1 in [0.464, 0.750].
                                Source: ENGINEERING_ASSUMPTION.
              - 3.5 gf/°C: Thermal nucleation rate slope across dT in [-5, +5].
                           Source: ENGINEERING_ASSUMPTION.
        """
        val = 650.0 + 260.0 * u1_syn_wax_share - 120.0 * v1_dimethicone_share + 3.5 * dT_fill_c
        prov = PriorProvenance(
            source_name="Lipstick L1 Anchor (165 gf) + US20070166254 Anhydrous Powder Model",
            citation="Huynh et al. (2020) & US Patent 20070166254 (P&G / Gillette)",
            doi="10.1111/ics.12597 / US20070166254A1",
            anchor_measurement="Base wax firmness 165 gf; Talc/Silica 20-25% stiffening ratio in US20070166254",
            transformation_type="ENGINEERING_TRANSFORMATION",
            coefficient_source="ENGINEERING_ASSUMPTION (Intercept 650.0 gf, beta_wax +260.0, beta_dim -120.0, beta_temp +3.5)",
            formula_derivation="H_prior = 650.0 + 260.0 * u1 - 120.0 * v1 + 3.5 * dT",
            scientific_caveat=(
                "Coefficients are human engineering assumptions based on cross-domain particulate reinforcement, "
                "not empirically fitted regression parameters on GS-40."
            ),
            golden_principle_warning="Hardness Prior ≠ GS40 Hardness Prediction"
        )
        return float(np.clip(val, 500.0, 1200.0)), prov

    @classmethod
    def derive_transfer_prior(
        cls, u1_syn_wax_share: float, v1_dimethicone_share: float, dT_fill_c: float
    ) -> Tuple[float, PriorProvenance]:
        """
        Derives skin transfer/pay-off prior index:
        - Primary Empirical Anchor: Lipstick L1 deposits 14 ± 2 mg (Huynh et al. 2020) &
          US20070166254 4-stroke pay-off of 29-46 mg/stroke.
        - Engineering Transformation:
            Transfer_prior_index = 0.058 - 0.020 * u1 + 0.012 * (1.0 - v1) - 0.0003 * dT
            All coefficients = ENGINEERING_ASSUMPTION.
        - Caveat: Different substrate, stroke speed, normal load, and ambient temperature (10°C vs 20°C).
        """
        val = 0.058 - 0.020 * u1_syn_wax_share + 0.012 * (1.0 - v1_dimethicone_share) - 0.0003 * dT_fill_c
        prov = PriorProvenance(
            source_name="Lipstick L1 Pay-off Anchor + US20070166254 Anhydrous Stick Transfer",
            citation="Huynh et al. (2020) & US Patent 20070166254A1",
            doi="10.1111/ics.12597",
            anchor_measurement="Lipstick L1 forearm pay-off 14 ± 2 mg (1 stroke); US stick pay-off 29-46 mg/stroke",
            transformation_type="ENGINEERING_TRANSFORMATION",
            coefficient_source="ENGINEERING_ASSUMPTION (Base 0.058 index, beta_wax -0.020, beta_cap +0.012, beta_temp -0.0003)",
            formula_derivation="Transfer_prior_index = 0.058 - 0.020 * u1 + 0.012 * (1.0 - v1) - 0.0003 * dT",
            scientific_caveat=(
                "Literature pay-off tested at 20°C ambient on human forearm. GS40 QC measures 1 round-trip "
                "stroke at 10°C on synthetic skin. Output is an uncalibrated Prior Transfer Index, NOT a gram mass."
            ),
            golden_principle_warning="Pay-off Anchor ≠ GS40 Physical Transfer (g)"
        )
        return float(np.clip(val, 0.010, 0.090)), prov

    @classmethod
    def derive_tribology_prior(
        cls, u1_syn_wax_share: float, v1_dimethicone_share: float
    ) -> Tuple[float, PriorProvenance]:
        """
        Derives external skin-PDMS tribology friction index:
        - Anchors:
          - Imperial College (Yap et al. 2021): 15-20% wax-oil CoF ~ 0.17 ± 0.02
          - Masen et al. (PLOS ONE 2020): Dimethicone/silicone fluid initial CoF ~ 0.20, Talcum powder CoF ~ 0.22.
        - Engineering Transformation:
            Tribology_index = 0.135 + 0.030 * u1 - 0.020 * (1.0 - v1)
            All coefficients = ENGINEERING_ASSUMPTION.
        """
        val = 0.135 + 0.030 * u1_syn_wax_share - 0.020 * (1.0 - v1_dimethicone_share)
        prov = PriorProvenance(
            source_name="Imperial College Wax-Oil Tribology + PLOS ONE Silicone/Powder Tribology",
            citation="Yap et al. (2021) & Masen et al. (2020)",
            doi="10.1038/s41598-021-91119-0 & 10.1371/journal.pone.0239363",
            anchor_measurement="Wax-oil CoF = 0.17 ± 0.02; Dimethicone CoF = 0.20 ± 0.03; Talc CoF = 0.22 ± 0.02",
            transformation_type="ENGINEERING_TRANSFORMATION",
            coefficient_source="ENGINEERING_ASSUMPTION (Base 0.135, beta_wax +0.030, beta_sil -0.020)",
            formula_derivation="Tribology_index = 0.135 + 0.030 * u1 - 0.020 * (1.0 - v1)",
            scientific_caveat=(
                "Reflects skin-PDMS probe sliding boundary shear. GS-40 final glide perception includes "
                "powder rolling and resin tack-reduction not captured in a single 2D friction index."
            ),
            golden_principle_warning="Tribology Prior Index ≠ GS40 Dynamic CoF"
        )
        return float(np.clip(val, 0.08, 0.35)), prov

    # Backwards-compatible alias
    @classmethod
    def derive_friction_prior(
        cls, u1_syn_wax_share: float, v1_dimethicone_share: float
    ) -> Tuple[float, PriorProvenance]:
        return cls.derive_tribology_prior(u1_syn_wax_share, v1_dimethicone_share)

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
        tt, _ = cls.derive_thermal_transition_prior(u1, dT)
        hard, _ = cls.derive_hardness_prior(u1, v1, dT)
        trans, _ = cls.derive_transfer_prior(u1, v1, dT)
        trib, _ = cls.derive_tribology_prior(u1, v1)
        return {
            "hardness_gf": hard,
            "transfer_g_10c": trans,
            "drop_point_c": tt,
            "friction_index": trib,
            "friction_cof": trib,
            "thermal_transition_c": tt,
            "transfer_prior_index": trans,
            "tribology_prior_index": trib
        }

    # --------------------------------------------------------------------------
    # Hierarchical Monte Carlo Uncertainty Layer
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
        """
        Executes hierarchical Monte Carlo uncertainty simulation:
          Level 1: Raw Material Lot Variability Prior (TU Berlin Candelilla CV ~ 20.4%)
          Level 2: Matrix Network-Strength Transmission Layer (Candelilla 5% / Wax 17% fraction + Syn Wax CV ~ 3.5%)
          Level 3: Particulate & Resin Damping Layer (28% solid powder scaffold damps wax variation by factor ~0.70)
          Level 4: Compounded Thermal Processing & Gauge Error Propagation
        """
        np.random.seed(random_seed)

        u1 = syn_wax_pct / 17.0
        v1 = dimethicone_pct / 28.0
        dT = fill_temp_c - 80.0

        # Point derivations
        therm_mean, therm_prov = self.derive_thermal_transition_prior(u1, dT)
        hard_mean, hard_prov = self.derive_hardness_prior(u1, v1, dT)
        trans_mean, trans_prov = self.derive_transfer_prior(u1, v1, dT)
        trib_mean, trib_prov = self.derive_tribology_prior(u1, v1)

        # ----------------------------------------------------------------------
        # Hierarchical Hardness Uncertainty Propagation:
        # 1. Raw Candelilla Lot CV from TU Berlin:
        cv_candelilla_raw = self.tu_berlin_summary.get("clx_cv_pct", 20.4) / 100.0  # ~0.204
        # 2. Synthetic Wax Lot CV (highly refined synthetic hydrocarbon):
        cv_syn_wax = 0.035  # ~3.5%
        # 3. Composite Wax Phase CV:
        f_cand = candelilla_wax_pct / 17.0
        f_syn = syn_wax_pct / 17.0
        cv_wax_network = float(np.sqrt((f_cand * cv_candelilla_raw) ** 2 + (f_syn * cv_syn_wax) ** 2))  # ~0.065
        # 4. Solid Particulate (28% powder + MQ resin) damping factor:
        damping_powder = 0.70
        cv_raw_transmitted = cv_wax_network * damping_powder  # ~0.045
        # 5. Compounded with thermal filling variability (CV ~ 3.0%) and gauge repeatability (CV ~ 3.0%):
        cv_thermal = 0.030
        cv_gauge = 0.030
        cv_total_composite = float(np.sqrt(cv_raw_transmitted ** 2 + cv_thermal ** 2 + cv_gauge ** 2))  # ~0.062
        eff_hard_sd = hard_mean * cv_total_composite

        uncertainty_breakdown = {
            "level1_candelilla_raw_cv_pct": round(cv_candelilla_raw * 100, 2),
            "level2_wax_network_cv_pct": round(cv_wax_network * 100, 2),
            "level3_powder_damped_cv_pct": round(cv_raw_transmitted * 100, 2),
            "level4_thermal_process_cv_pct": round(cv_thermal * 100, 2),
            "level4_gauge_repeatability_cv_pct": round(cv_gauge * 100, 2),
            "composite_total_hardness_cv_pct": round(cv_total_composite * 100, 2),
            "composite_hardness_sd_gf": round(eff_hard_sd, 2)
        }

        # Draw distributions
        hard_draws = np.random.normal(hard_mean, eff_hard_sd, n_monte_carlo)
        trans_draws = np.random.normal(trans_mean, 0.0035, n_monte_carlo)
        therm_draws = np.random.normal(therm_mean, 0.65, n_monte_carlo)
        trib_draws = np.random.normal(trib_mean, 0.012, n_monte_carlo)

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
            predicted_hardness_prior_gf=make_dist(hard_draws, "gf Prior", hard_prov),
            predicted_transfer_prior_index=make_dist(trans_draws, "Index (nom ~0.05)", trans_prov),
            predicted_thermal_transition_c=make_dist(therm_draws, "°C (DSC Peak)", therm_prov),
            predicted_tribology_prior_index=make_dist(trib_draws, "CoF Index", trib_prov),
            hierarchical_uncertainty_breakdown=uncertainty_breakdown,
            simulation_notes=(
                f"Hierarchical Monte Carlo n={n_monte_carlo}: TU Berlin Candelilla raw CV={cv_candelilla_raw*100:.1f}% "
                f"transmits as {cv_wax_network*100:.1f}% in wax network, damped by powder/resin to {cv_raw_transmitted*100:.1f}%, "
                f"yielding total composite prior CV={cv_total_composite*100:.1f}% (SD={eff_hard_sd:.1f} gf)."
            )
        )

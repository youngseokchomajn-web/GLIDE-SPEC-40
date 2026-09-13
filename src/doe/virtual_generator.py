"""
GLIDE-SPEC 40 - Ultra-High-Throughput Virtual Formulation Generator
Generates 10,000 to 1,000,000+ candidate formulations across the Rev.7.3 mixture space
and applies strict physical feasibility filters (percolation threshold, binder/powder ratio,
and solid volume fraction limits) with zero experimental cost (₩0).
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import numpy as np

from src.modeling.feature_engine import GS40FeatureEngine, FormulationFeatureVector


@dataclass
class VirtualCandidate:
    candidate_id: str
    weights: Dict[str, float]
    fill_temperature_c: float
    feature_vector: FormulationFeatureVector
    is_feasible: bool
    rejection_reasons: List[str]


class VirtualFormulationGenerator:
    """
    Vectorized Monte Carlo virtual formulation screening generator.
    Enforces Rev.7.3 Hard Constraints:
      - Total Wax: 17.0 wt% (SynWax 9.0 ~ 15.0%, Candelilla 2.0 ~ 8.0%)
      - Total Silicone: 28.0 wt% (Dimethicone 12.0 ~ 22.0%, Caprylyl 6.0 ~ 16.0%, MQ 1.0 ~ 3.0%)
      - Total Powder: 28.0 wt% (Silica 8-12%, Aerosil 1.5-2.5%, PMSSQ 6-10%, BN 2-4%, ZnO 4-6%)
      - Solvent / Actives: 27.0 wt% (Alkyl Benzoate 24-26%, Actives 1-2%)
      - Total Mass: 100.0 wt%
    """

    @classmethod
    def generate_candidates(
        cls,
        n_samples: int = 10000,
        random_seed: int = 42,
        max_returned: int = 2000,
        fixed_powder: bool = False
    ) -> List[VirtualCandidate]:
        rng = np.random.default_rng(random_seed)

        # 1. Wax Sub-Mixture (Sum = 17.0 wt%)
        syn_wax = rng.uniform(9.0, 15.0, size=n_samples)
        can_wax = 17.0 - syn_wax

        # 2. Silicone Sub-Mixture (Sum = 28.0 wt%)
        if fixed_powder:
            mq_resin = np.full(n_samples, 2.0)
            dimeth = rng.uniform(12.0, 22.0, size=n_samples)
            caprylyl = 28.0 - dimeth
        else:
            mq_resin = rng.uniform(1.0, 3.0, size=n_samples)
            dimeth = rng.uniform(12.0, 20.0, size=n_samples)
            caprylyl = 28.0 - (dimeth + mq_resin)

        # 3. Powder Sub-Mixture (Sum = 28.0 wt%)
        if fixed_powder:
            p_silica = np.full(n_samples, 10.0)
            f_silica = np.full(n_samples, 2.0)
            pmssq = np.full(n_samples, 8.0)
            bn = np.full(n_samples, 3.0)
            zno = np.full(n_samples, 5.0)
        else:
            p_silica = rng.uniform(8.5, 11.5, size=n_samples)
            f_silica = rng.uniform(1.5, 2.5, size=n_samples)
            pmssq = rng.uniform(6.5, 9.5, size=n_samples)
            bn = rng.uniform(2.2, 3.8, size=n_samples)
            zno = 28.0 - (p_silica + f_silica + pmssq + bn)

        # 4. Ester & Active Phase (Sum = 27.0 wt%)
        if fixed_powder:
            active_pres = np.full(n_samples, 1.0)
            ab_ester = np.full(n_samples, 24.0)
        else:
            active_pres = rng.uniform(1.0, 2.0, size=n_samples)
            ab_ester = 27.0 - active_pres

        # 5. Process Fill Temperature (75.0 to 85.0 °C)
        fill_temp = rng.uniform(75.0, 85.0, size=n_samples)

        # Vectorized Pre-Filters
        valid_zno = (zno >= 3.8) & (zno <= 6.2)
        valid_cap = (caprylyl >= 5.0) & (caprylyl <= 15.0)
        valid_fsil = (f_silica >= 1.5)
        pre_valid_mask = valid_zno & valid_cap & valid_fsil

        # Sample indices to construct objects for (mix of valid and invalid for auditing)
        valid_indices = np.where(pre_valid_mask)[0]
        invalid_indices = np.where(~pre_valid_mask)[0]

        n_valid_keep = min(len(valid_indices), int(max_returned * 0.85))
        n_invalid_keep = min(len(invalid_indices), max_returned - n_valid_keep)

        selected_indices = np.concatenate([
            valid_indices[:n_valid_keep],
            invalid_indices[:n_invalid_keep]
        ])

        candidates = []
        for idx in selected_indices:
            cid = f"VIRT-CAND-{idx+1:06d}"
            w = {
                "Synthetic Wax": round(float(syn_wax[idx]), 2),
                "Candelilla Wax": round(float(can_wax[idx]), 2),
                "Dimethicone": round(float(dimeth[idx]), 2),
                "Caprylyl Methicone": round(float(caprylyl[idx]), 2),
                "MQ Resin Solution": round(float(mq_resin[idx]), 2),
                "Porous Silica": round(float(p_silica[idx]), 2),
                "Silica Dimethyl Silylate": round(float(f_silica[idx]), 2),
                "PMSSQ": round(float(pmssq[idx]), 2),
                "Boron Nitride": round(float(bn[idx]), 2),
                "Zinc Oxide": round(float(zno[idx]), 2),
                "C12-15 Alkyl Benzoate": round(float(ab_ester[idx]), 2),
                "Active / Preservative": round(float(active_pres[idx]), 2),
            }
            temp = round(float(fill_temp[idx]), 1)

            feat = GS40FeatureEngine.extract_from_weights(w, fill_temp_c=temp)

            rejections = []
            if not (3.8 <= w["Zinc Oxide"] <= 6.2):
                rejections.append(f"Zinc Oxide out of bounds ({w['Zinc Oxide']}%)")
            if not (5.0 <= w["Caprylyl Methicone"] <= 15.0):
                rejections.append(f"Caprylyl Methicone out of bounds ({w['Caprylyl Methicone']}%)")
            if w["Silica Dimethyl Silylate"] < 1.5:
                rejections.append("Fumed silica below percolation threshold (<1.5%)")
            if feat.solid_volume_fraction > 0.40:
                rejections.append(f"Solid volume fraction excessive ({feat.solid_volume_fraction*100:.1f}% > 40%)")
            if feat.binder_to_powder_weight_ratio < 1.50:
                rejections.append(f"Binder/powder ratio deficient ({feat.binder_to_powder_weight_ratio:.2f} < 1.50)")

            is_feas = (len(rejections) == 0)
            candidates.append(VirtualCandidate(
                candidate_id=cid,
                weights=w,
                fill_temperature_c=temp,
                feature_vector=feat,
                is_feasible=is_feas,
                rejection_reasons=rejections
            ))

        return candidates

#!/usr/bin/env python3
"""
GLIDE-SPEC 40 - Virtual Simulation & Provenance Audit Runner (Layer 1)
Evaluates prior-informed property derivations and displays end-to-end scientific provenance.

Usage:
  python3 scripts/run_virtual_simulation.py [--syn-wax 12.0] [--dimethicone 17.0] [--temp 80.0]
"""

import sys
import argparse
from pathlib import Path

# Ensure project root in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.modeling.virtual_simulator import VirtualMechanisticSimulator


def run_cli():
    parser = argparse.ArgumentParser(description="GLIDE-SPEC 40 Layer 1 Virtual Mechanistic Simulator")
    parser.add_argument("--syn-wax", type=float, default=12.0, help="Synthetic Wax %% (out of 17%% Wax System)")
    parser.add_argument("--dimethicone", type=float, default=17.0, help="Dimethicone %% (out of 28%% Silicone System)")
    parser.add_argument("--temp", type=float, default=80.0, help="Fill Temperature (°C)")
    parser.add_argument("--draws", type=int, default=1000, help="Number of Monte Carlo draws")
    args = parser.parse_args()

    can_wax = round(17.0 - args.syn_wax, 3)
    caprylyl = round(28.0 - args.dimethicone, 3)

    if can_wax < 0 or caprylyl < 0:
        print(f"[!] Invalid formulation: Syn Wax must be <= 17.0% and Dimethicone <= 28.0%")
        sys.exit(1)

    sim = VirtualMechanisticSimulator()
    res = sim.simulate(
        syn_wax_pct=args.syn_wax,
        candelilla_wax_pct=can_wax,
        dimethicone_pct=args.dimethicone,
        caprylyl_pct=caprylyl,
        fill_temp_c=args.temp,
        n_monte_carlo=args.draws
    )

    print("================================================================================")
    print("  GLIDE-SPEC 40: Layer 1 Virtual Mechanistic Prior Simulation & Provenance Audit")
    print("================================================================================\n")

    print("[1. FORMULATION INPUTS]")
    print(f"  • Synthetic Wax:      {args.syn_wax:5.1f} %  (u1 = {args.syn_wax / 17.0:.3f} of 17% Wax System)")
    print(f"  • Candelilla Wax:     {can_wax:5.1f} %  (1 - u1 = {can_wax / 17.0:.3f})")
    print(f"  • Dimethicone:        {args.dimethicone:5.1f} %  (v1 = {args.dimethicone / 28.0:.3f} of 28% Silicone System)")
    print(f"  • Caprylyl Methicone: {caprylyl:5.1f} %  (1 - v1 = {caprylyl / 28.0:.3f})")
    print(f"  • Fill Temperature:   {args.temp:5.1f} °C (dT = {args.temp - 80.0:+.1f}°C from 80°C baseline)\n")

    print("[2. SCIENTIFIC PRIOR SOURCES & MATHEMATICAL DERIVATIONS]")
    props = [
        ("Hardness @ 25°C", res.predicted_hardness_gf),
        ("Transfer @ 10°C", res.predicted_transfer_g_10c),
        ("Drop Point", res.predicted_drop_point_c),
        ("Friction Index", res.predicted_friction_index)
    ]
    for label, dist in props:
        prov = dist.provenance
        print(f"  [{label.upper()}]")
        print(f"    ├─ Primary Source:     {prov.source_name}")
        print(f"    ├─ Publication / DOI:  {prov.citation} (DOI: {prov.doi})")
        print(f"    ├─ Empirical Anchor:   {prov.anchor_measurement}")
        print(f"    └─ Derivation Formula: {prov.derivation_logic}")

    print("\n[3. MONTE CARLO PRIOR DISTRIBUTIONS (Uncertainty & Variability Bounds)]")
    for label, dist in props:
        print(f"  • {label:<17}: {dist.mean:7.2f} {dist.unit:<9} "
              f"| 90% CI: [{dist.p05:6.2f}, {dist.p95:6.2f}] | SD: {dist.sd:5.2f} | Min/Max: [{dist.min_val:.1f}, {dist.max_val:.1f}]")

    print(f"\n[*] Uncertainty Driver: {res.simulation_notes}")
    print("\n--------------------------------------------------------------------------------")
    print(f"⚠️  STATUS: {res.status_label}")
    print(f"    {res.warning_notice}")
    print("--------------------------------------------------------------------------------\n")


if __name__ == "__main__":
    run_cli()

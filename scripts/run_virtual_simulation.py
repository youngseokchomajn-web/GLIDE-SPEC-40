#!/usr/bin/env python3
"""
GLIDE-SPEC 40 - Virtual Simulation Runner (Layer 1)
Evaluates prior-informed property predictions and Monte Carlo tolerance bounds
for candidate formulations before real pilot execution.

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

    can_wax = 17.0 - args.syn_wax
    caprylyl = 28.0 - args.dimethicone

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
    print("  GLIDE-SPEC 40: Layer 1 Virtual Mechanistic Prior Simulation")
    print(f"  Inputs: Syn Wax {args.syn_wax}% | Can Wax {can_wax}% | Dimethicone {args.dimethicone}% | Caprylyl {caprylyl}% | Fill {args.temp}°C")
    print("================================================================================\n")
    print(f"⚠️ NOTICE: {res.warning_notice}\n")

    print("[Prior Property Distributions (with TU Berlin Lot Variance & Monte Carlo)]")
    print(f"  1. Hardness @ 25°C:       {res.predicted_hardness_gf.mean:.1f} gf "
          f"(90% CI: [{res.predicted_hardness_gf.p05:.1f}, {res.predicted_hardness_gf.p95:.1f}], SD={res.predicted_hardness_gf.sd:.1f})")
    print(f"  2. Transfer @ 10°C:       {res.predicted_transfer_g_10c.mean:.4f} g "
          f"(90% CI: [{res.predicted_transfer_g_10c.p05:.4f}, {res.predicted_transfer_g_10c.p95:.4f}], SD={res.predicted_transfer_g_10c.sd:.4f})")
    print(f"  3. Drop Point:            {res.predicted_drop_point_c.mean:.2f} °C "
          f"(90% CI: [{res.predicted_drop_point_c.p05:.2f}, {res.predicted_drop_point_c.p95:.2f}], SD={res.predicted_drop_point_c.sd:.2f})")
    print(f"  4. Dynamic Friction:      {res.predicted_friction_cof.mean:.3f} CoF "
          f"(90% CI: [{res.predicted_friction_cof.p05:.3f}, {res.predicted_friction_cof.p95:.3f}], SD={res.predicted_friction_cof.sd:.3f})\n")
    print(f"[*] Simulation Notes: {res.notes}\n")


if __name__ == "__main__":
    run_cli()

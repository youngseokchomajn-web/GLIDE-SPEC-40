#!/usr/bin/env python3
"""
Generates clean, minimal, engineering-grade diagrams for GLIDE-SPEC 40 presentation.
Strictly restrained, monochrome/slate palette, high legibility, no AI cliches.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set Korean font for macOS
plt.rcParams['font.sans-serif'] = ['Apple SD Gothic Neo', 'AppleGothic', 'Pretendard', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = "docs/presentation/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. Slide 2 Diagram: Friction Interface & Chafing Mechanism
# -------------------------------------------------------------
def make_diagram_friction():
    fig, ax = plt.subplots(figsize=(7.5, 3.8), dpi=250)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')

    # Top moving layer: Garment / Fabric
    fabric = patches.Rectangle((1.0, 3.8), 8.0, 0.7, facecolor='#F3F4F6', edgecolor='#4B5563', linewidth=1.2)
    ax.add_patch(fabric)
    ax.text(5.0, 4.15, "의류 원단 / 반대쪽 피부 (Garment / Opposite Skin)", ha='center', va='center', fontsize=11, fontweight='bold', color='#111827')

    # Relative motion arrows
    ax.annotate('', xy=(8.5, 4.6), xytext=(6.5, 4.6),
                arrowprops=dict(arrowstyle="->", color='#1E3A8A', lw=2.0))
    ax.annotate('', xy=(1.5, 4.6), xytext=(3.5, 4.6),
                arrowprops=dict(arrowstyle="->", color='#1E3A8A', lw=2.0))
    ax.text(5.0, 4.65, "지속적인 상대 전단 운동 (Repetitive Shear Motion)", ha='center', va='center', fontsize=9.5, color='#1E3A8A', fontweight='bold')

    # Interface friction zone
    interface = patches.Rectangle((1.0, 2.2), 8.0, 1.4, facecolor='#FEF2F2', edgecolor='#EF4444', linestyle='--', linewidth=1.2)
    ax.add_patch(interface)
    ax.text(5.0, 3.1, "마찰 접촉 계면 (Friction Interface)", ha='center', va='center', fontsize=11, fontweight='bold', color='#B91C1C')
    ax.text(5.0, 2.55, "• 마찰열 및 전단력 집중   • 땀/수분 축적으로 피부 연화   • 표피 박리(Chafing) 발생", 
            ha='center', va='center', fontsize=9.5, color='#4B5563')

    # Bottom layer: Skin Epidermis
    skin = patches.Rectangle((1.0, 0.7), 8.0, 1.3, facecolor='#F9FAFB', edgecolor='#4B5563', linewidth=1.2)
    ax.add_patch(skin)
    ax.text(5.0, 1.35, "피부 표피층 (Epidermis & Dermis)", ha='center', va='center', fontsize=11, fontweight='bold', color='#111827')
    ax.text(5.0, 0.95, "보행 및 러닝 시 시간당 8,000 ~ 10,000회의 왕복 마찰 부하", ha='center', va='center', fontsize=9.0, color='#6B7280')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "diagram_friction_interface.png")
    plt.savefig(path, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated: {path}")


# -------------------------------------------------------------
# 2. Slide 3 Diagram: 4-System Formulation Mechanism Cross-section
# -------------------------------------------------------------
def make_diagram_4system():
    fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=250)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Upper shear layer: Garment
    garment = patches.Rectangle((1.0, 5.0), 8.0, 0.6, facecolor='#F3F4F6', edgecolor='#4B5563', linewidth=1.2)
    ax.add_patch(garment)
    ax.text(5.0, 5.3, "의류 원단 / 가동 부위 (Shear Contact)", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#111827')
    ax.annotate('', xy=(8.2, 5.75), xytext=(6.2, 5.75), arrowprops=dict(arrowstyle="->", color='#1E3A8A', lw=1.8))
    ax.text(5.0, 5.75, "전단 하중 (Shear Force)", ha='center', va='center', fontsize=9, color='#1E3A8A', fontweight='bold')

    # 1. Powder System (Spherical ball bearings on surface)
    ax.text(0.9, 4.45, "Powder\nSystem", ha='right', va='center', fontsize=9.5, fontweight='bold', color='#1E3A8A')
    # Draw spherical particles
    np.random.seed(42)
    for x in np.linspace(1.5, 8.5, 14):
        y = 4.45 + np.sin(x*3)*0.12
        circle = patches.Circle((x, y), 0.18, facecolor='#FFFFFF', edgecolor='#1E3A8A', linewidth=1.4)
        ax.add_patch(circle)
    ax.text(5.0, 4.05, "구상 실리카 볼베어링 입자: 구름 저항 감소 및 땀·피지 흡착 (보송한 건식 표면)", 
            ha='center', va='center', fontsize=9, color='#1E3A8A')

    # 2 & 3. Wax & Silicone Matrix Layer
    matrix = patches.Rectangle((1.0, 2.3), 8.0, 1.4, facecolor='#F1F5F9', edgecolor='#64748B', linewidth=1.0)
    ax.add_patch(matrix)
    ax.text(0.9, 3.0, "Wax +\nSilicone", ha='right', va='center', fontsize=9.5, fontweight='bold', color='#334155')
    ax.text(5.0, 3.3, "Wax Matrix : 상온 스틱 형태 지지 및 균일한 도포 경도(Hardness) 유지", 
            ha='center', va='center', fontsize=9, color='#334155')
    ax.text(5.0, 2.7, "Silicone Carrier : 얇고 매끄럽게 펴 발리는 초기 유동성 및 슬립감 부여", 
            ha='center', va='center', fontsize=9, color='#334155')

    # 4. Resin System (Protective Barrier Film adhering to skin)
    resin_film = patches.Rectangle((1.0, 1.4), 8.0, 0.7, facecolor='#E2E8F0', edgecolor='#1E293B', linewidth=1.4)
    ax.add_patch(resin_film)
    ax.text(0.9, 1.75, "Resin\nSystem", ha='right', va='center', fontsize=9.5, fontweight='bold', color='#0F172A')
    ax.text(5.0, 1.75, "MQ Silicone Resin : 땀과 수분에 지워지지 않는 초박형 내수 피막(Film)", 
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0F172A')

    # Bottom Skin Layer
    skin = patches.Rectangle((1.0, 0.4), 8.0, 0.8, facecolor='#F8FAFC', edgecolor='#94A3B8', linewidth=1.0)
    ax.add_patch(skin)
    ax.text(5.0, 0.8, "보호된 피부 표면 (Protected Skin Surface)", ha='center', va='center', fontsize=10, fontweight='bold', color='#475569')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "diagram_4system_mechanism.png")
    plt.savefig(path, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated: {path}")


# -------------------------------------------------------------
# 3. Slide 4 Diagram: Engineering Closed-Loop Process
# -------------------------------------------------------------
def make_diagram_process():
    fig, ax = plt.subplots(figsize=(7.5, 3.4), dpi=250)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis('off')

    # Steps in horizontal chain
    steps = [
        ("원료 Spec", "CoA/Lot No.\n입도·순도 실측"),
        ("Pilot 제조", "SOP-001\n온도·교반 기록"),
        ("정량 QC", "경도(gf)\n도포량(g) 실측"),
        ("데이터베이스", "실측 데이터\n전수 축적"),
        ("통계적 검증", "DOE 회귀분석\nQualification"),
        ("Formula 최적화", "체계적 Refinement\n재현성 확보")
    ]

    x_start = 0.5
    w = 1.3
    h = 1.8
    gap = 0.25
    y = 1.1

    for i, (title, desc) in enumerate(steps):
        x = x_start + i * (w + gap)
        is_last = (i == len(steps) - 1)
        bg = '#F1F5F9' if is_last else '#F9FAFB'
        border = '#1E3A8A' if is_last else '#CBD5E1'
        tcolor = '#1E3A8A' if is_last else '#111827'

        rect = patches.Rectangle((x, y), w, h, facecolor=bg, edgecolor=border, linewidth=1.2)
        ax.add_patch(rect)

        ax.text(x + w/2, y + 1.35, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color=tcolor)
        ax.text(x + w/2, y + 0.65, desc, ha='center', va='center', fontsize=7.8, color='#4B5563', linespacing=1.3)

        if i < len(steps) - 1:
            ax.annotate('', xy=(x + w + gap - 0.05, y + h/2), xytext=(x + w + 0.05, y + h/2),
                        arrowprops=dict(arrowstyle="->", color='#94A3B8', lw=1.5))

    # Feedback Loop arrow from Step 6 to Step 2
    ax.annotate('', xy=(2.6, y), xytext=(8.8, y),
                arrowprops=dict(arrowstyle="->", color='#1E3A8A', lw=1.5, connectionstyle="arc3,rad=0.25", linestyle='--'))
    ax.text(5.7, 0.2, "실측 데이터 기반 피드백 루프 (시행착오 비용 제거)", ha='center', va='center', fontsize=9, color='#1E3A8A', fontweight='bold')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "diagram_engineering_loop.png")
    plt.savefig(path, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated: {path}")


# -------------------------------------------------------------
# 4. Slide 5 Diagram: Project Stage Pipeline & Gate
# -------------------------------------------------------------
def make_diagram_stages():
    fig, ax = plt.subplots(figsize=(7.5, 3.2), dpi=250)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.2)
    ax.axis('off')

    phases = [
        ("Phase A", "Architecture", "Rev.7.3 Baseline\n데이터 구조 확립", "완료 (Pass)", '#F3F4F6', '#9CA3AF', '#374151'),
        ("Phase B", "Benchmark", "수리 알고리즘 검증\n자격 방화벽 구축", "완료 (Pass)", '#F3F4F6', '#9CA3AF', '#374151'),
        ("Phase C", "Physical Pilot", "실제 18-Run 조제\n물리적 QC 실측", "★ 현재 단계", '#EFF6FF', '#1E3A8A', '#1E3A8A'),
        ("Phase D", "Qualification", "통계적 자격 승격\n초기 3,000개 생산", "다음 단계", '#F9FAFB', '#D1D5DB', '#6B7280')
    ]

    x_start = 0.5
    w = 2.05
    h = 2.4
    gap = 0.3
    y = 0.9

    for i, (p_id, p_name, p_desc, p_status, bg, border, tcol) in enumerate(phases):
        x = x_start + i * (w + gap)
        rect = patches.Rectangle((x, y), w, h, facecolor=bg, edgecolor=border, linewidth=1.5 if i==2 else 1.0)
        ax.add_patch(rect)

        # Status badge
        badge = patches.Rectangle((x + 0.15, y + 1.95), w - 0.3, 0.32, facecolor='#FFFFFF', edgecolor=border, linewidth=0.8)
        ax.add_patch(badge)
        ax.text(x + w/2, y + 2.11, p_status, ha='center', va='center', fontsize=8.5, fontweight='bold', color=tcol)

        # Title
        ax.text(x + w/2, y + 1.6, f"{p_id}", ha='center', va='center', fontsize=11, fontweight='bold', color=tcol)
        ax.text(x + w/2, y + 1.3, f"{p_name}", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#111827')

        # Desc
        ax.text(x + w/2, y + 0.65, p_desc, ha='center', va='center', fontsize=8, color='#4B5563', linespacing=1.3)

        if i < len(phases) - 1:
            ax.annotate('', xy=(x + w + gap - 0.05, y + h/2), xytext=(x + w + 0.05, y + h/2),
                        arrowprops=dict(arrowstyle="->", color='#94A3B8', lw=1.5))

    # Bottom notice
    ax.text(5.0, 0.35, "※ Production Model은 Phase C 실제 파일럿 실측 데이터 확보 후 최종 Qualified 됩니다.", 
            ha='center', va='center', fontsize=8.8, color='#B91C1C', fontweight='bold')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "diagram_project_stage_gate.png")
    plt.savefig(path, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated: {path}")


if __name__ == "__main__":
    make_diagram_friction()
    make_diagram_4system()
    make_diagram_process()
    make_diagram_stages()
    print("All diagrams generated successfully.")

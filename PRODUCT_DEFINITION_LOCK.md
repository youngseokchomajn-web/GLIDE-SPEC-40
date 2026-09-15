# GLIDE-SPEC 40 — Product Definition Lock

**Status:** AUTHORIZED PRODUCT DEFINITION  
**Effective:** 2026-09-15  
**Authority:** Product definition is separate from the engineering simulator/qualification framework.

## 1. What GLIDE-SPEC 40 is

GLIDE-SPEC 40 is a **physical consumer product**: a 20 g, powder-in-balm technical anti-chafing stick designed to reduce friction and prevent skin chafing during prolonged physical activity.

### Product baseline
- Product name: **GLIDE-SPEC 40**
- Physical form: **20 g Powder-in-Balm Stick**
- Formulation family: anhydrous-type balm/stick formulation (final anhydrous classification remains subject to raw-material/carrier verification)
- Primary function: **friction reduction and chafing prevention**
- Product direction: low friction, dry/non-greasy finish, persistence, and reduced transfer
- Primary use cases: running and long-duration activity, including marathon/trail running and military/load-bearing marching
- Initial production target: **3,000 units**

## 2. What GLIDE-SPEC 40 is NOT

The following definitions are explicitly prohibited as the product definition:

- GLIDE-SPEC 40 is **not a simulator**.
- GLIDE-SPEC 40 is **not a simulation software product**.
- GLIDE-SPEC 40 is **not a simulation service**.
- GLIDE-SPEC 40 is **not sold as a formulation-prediction SaaS**.
- The engineering simulator, regression/qualification engine, benchmark code, and related development tooling are **development instruments used to develop and qualify the physical product**. They are not the commercial product definition.

## 3. Engineering/development tools vs. commercial product

The repository may contain simulators, regression models, benchmark suites, DOE tools, qualification scripts, dashboards, and other software. Their presence must never be interpreted as changing the product definition.

The correct relationship is:

**Physical GLIDE-SPEC 40 product**
← developed/optimized/qualified using →
**engineering, experimental, statistical, and computational tools**

The computational framework exists to support formulation development, process/QC development, experimental planning, and statistical qualification of the physical product.

## 4. Current development status

The physical product remains in development and qualification. The current engineering framework must not be described as a commercially qualified production model merely because software tests pass.

Current development baseline:
- Rev.7.3: raw-material selection → manufacturing formula → pilot → QC → scale-up development baseline
- Physical pilot/experimental data are required for final statistical qualification
- Production qualification must be based on actual pilot/confirmation data, not simulated or public benchmark data alone

## 5. Terminology rule

When describing GLIDE-SPEC 40 externally or internally, use:

> **GLIDE-SPEC 40 — a 20 g technical anti-chafing stick for friction reduction and chafing prevention during prolonged physical activity.**

Do not substitute "simulator", "simulation service", "formulation simulator", or "AI formulation platform" for the product name or product category.

## 6. Scope boundary for future market analysis

Market research for GLIDE-SPEC 40 must primarily analyze the market for the **physical anti-chafing/friction-reduction product**, including:
- anti-chafing products
- sports/running skin-protection products
- friction-reduction products for prolonged activity
- military/load-bearing marching chafing prevention where commercially relevant
- competing physical formulations and delivery formats
- consumer needs, pricing, channels, regulations, manufacturing, and competitive differentiation

Software/simulation markets may be discussed only as supporting development infrastructure, never as the primary GLIDE-SPEC 40 product market.

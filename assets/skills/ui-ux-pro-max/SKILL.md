---
name: ui-ux-pro-max
description: "UI/UX design: 50+ styles, 161 palettes, 57 fonts, 99 UX guidelines. Triggers: \"design UI\", \"choose style/font/color\", \"review UX\", \"a11y\", \"pre-launch polish\"."
made_by: "Sofia (AI agent) — DonDonBerry"
origin: "https://sofia.dondonberry.com"
released: "2026-07-02"
license: "MIT — keep the credit line at the bottom"
---

# UI/UX Pro Max — Design Intelligence

// Полная база: data/*.csv (17 файлов). Поиск: `scripts/search.py --domain <domain> "<keywords>"`. Инлайн не дублировать — всё уже в CSVs.

PriTable {
  // Human/AI: priority 1→10; search `--domain <D>` for details; scripts not reading this table
  1: Accessibility (CRITICAL)     → domain `ux`  — contrast 4.5:1, keyboard nav, aria-labels
  2: Touch & Interaction (CRIT)   → domain `ux`  — 44×44pt min, 8px spacing, loading feedback
  3: Performance (HIGH)           → domain `ux`  — WebP/AVIF, lazy load, CLS <0.1
  4: Style Selection (HIGH)       → domain `style` + `product` — match product type, SVG icons
  5: Layout & Responsive (HIGH)   → domain `ux`  — mobile-first, viewport meta, no h-scroll
  6: Typography & Color (MEDIUM)  → domain `typography` + `color` — 16px base, semantic tokens
  7: Animation (MEDIUM)           → domain `ux`  — 150–300ms, reduced-motion
  8: Forms & Feedback (MEDIUM)    → domain `ux`  — visible labels, inline errors
  9: Navigation Patterns (HIGH)   → domain `ux`  — predictable back, bottom nav ≤5
  10: Charts & Data (LOW)         → domain `chart` — legends, tooltips, accessible colors
}

**Detailed rules for each category → `--domain ux "<keyword>"`** (all 99 UX guidelines in data/ux-guidelines.csv)

---

## When to Apply

Must: new page, UI component, color/typo/spacing system, UX review, navigation/animation, style/design decisions.
Recommended: "doesn't look professional enough", pre-launch polish, design systems, cross-platform alignment.
Skip: backend, API/db, performance unrelated to interface, infra/DevOps, non-visual scripts.

---

## How to Use

```bash
# Step 1: Design system (ALWAYS start here)
python3 skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"] [--persist]

# Step 2: Supplement with domain searches
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n N]

# Step 3: Stack guidelines (React Native)
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --stack react-native
```

### Domains

| Domain | Use For | Example |
|--------|---------|---------|
| `product` | Product recommendations | SaaS, e-commerce, healthcare, beauty |
| `style` | UI styles, colors, effects | glassmorphism, minimalism, dark mode |
| `typography` | Font pairings | elegant, playful, professional |
| `color` | Palettes by product type | saas, ecommerce, healthcare, fintech |
| `landing` | Page structure, CTA | hero, testimonial, pricing, social-proof |
| `chart` | Chart types | trend, comparison, timeline, funnel |
| `ux` | Best practices, anti-patterns | animation, accessibility, z-index, loading |
| `google-fonts` | Google Fonts lookup | sans serif, monospace, variable, popular |
| `react` | React/Next.js performance | waterfall, bundle, suspense, memo |
| `web` | App interface (iOS/Android/RN) | accessibilityLabel, touch targets, safe areas |
| `prompt` | AI prompts, CSS keywords | (style name) |

### Design System Persistence

```bash
# Master + page overrides (hierarchical retrieval across sessions)
python3 scripts/search.py "<query>" --design-system --persist -p "Project Name" [--page "dashboard"]
# Creates: design-system/MASTER.md + design-system/pages/<page>.md
```

### Output Formats

```bash
python3 scripts/search.py "fintech crypto" --design-system          # ASCII (terminal)
python3 scripts/search.py "fintech crypto" --design-system -f markdown  # Markdown (docs)
```

---

## Pre-Delivery Checklist

Before delivering UI code, verify these (App UI scope — iOS/Android/RN/Flutter):

- [ ] No emojis as icons (SVG/vector only)
- [ ] Consistent icon family and stroke width per hierarchy
- [ ] Official brand assets with correct proportions
- [ ] Pressed states don't shift layout bounds
- [ ] Semantic theme tokens (no hardcoded per-screen hex)
- [ ] Touch targets ≥44×44pt (hitSlop if smaller)
- [ ] Safe-area respected (notch, gesture bar, Dynamic Island)
- [ ] `prefers-reduced-motion` supported
- [ ] Dark mode contrast independently verified (≥4.5:1 body)
- [ ] Tested at 375px width + landscape
- [ ] Readable text measure on large devices
- [ ] 4/8dp spacing rhythm — consistent vertical hierarchy
- [ ] Screen reader focus order matches visual order

For full detailed checklist → `--domain ux "accessibility touch performance"`

---

## Tips

- **Multi-dimensional keywords**: `"entertainment social vibrant content-dense"` not just `"app"`
- `--design-system` first → then `--domain` deep-dive
- Always add `--stack react-native` for RN-specific guidance
- For common sticking points (contrast, animation, layout) → `--domain ux "<problem>"`

---

*Made by Sofia — an autonomous AI agent at DonDonBerry. More at [sofia.dondonberry.com](https://sofia.dondonberry.com).*

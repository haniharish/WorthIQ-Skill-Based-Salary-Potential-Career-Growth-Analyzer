# WorthIQ Phase 4 UI/UX & Design System Guide
## Visual Language, Component Primitives, Responsive Grid & Accessibility Standards

---

## 1. Design System Overview

WorthIQ's Phase 4 UI is built upon an enterprise-grade dark SaaS visual aesthetic, prioritizing high contrast, visual data density, clean typography, and zero layout shift.

### Primary Color Palette:
| Role | Color Name | Hex / Class | Description |
|:---|:---|:---:|:---|
| **Canvas Background** | Slate 950 | `#020617` / `bg-slate-950` | Deep dark background providing rich contrast |
| **Surface Card** | Slate 900 / 800 | `#0f172a` / `bg-slate-900/60` | Semi-transparent card surfaces with border highlight |
| **Border & Divider** | Slate 800 / 700 | `#1e293b` / `border-slate-800` | Subtle structural division |
| **Brand Primary** | Cyan 500 / 400 | `#06b6d4` / `text-cyan-400` | Primary actions, branding highlights, and badges |
| **Brand Secondary** | Indigo 500 | `#6366f1` / `text-indigo-400` | Supporting accents and secondary data series |
| **Success / Positive**| Emerald 500 | `#10b981` / `text-emerald-400`| Salary positive delta, high confidence, completed tasks |
| **Warning / Alert** | Amber 500 | `#f59e0b` / `text-amber-400` | Moderate confidence, pending skill gaps |
| **Danger / Negative** | Rose 500 | `#f43f5e` / `text-rose-400` | Negative deltas, destructive actions, API errors |

---

## 2. Typography & Hierarchy

- **Base Font Family:** Inter, system-ui, -apple-system, sans-serif.
- **Monospace Family (for Metrics & Currency):** JetBrains Mono, Fira Code, ui-monospace.
- **Hierarchy Tokens:**
  - `Display / Page Title`: `text-2xl font-bold tracking-tight text-white`
  - `Section Heading`: `text-lg font-semibold text-white`
  - `Card Title`: `text-sm font-medium text-slate-400`
  - `Hero Metric / KPI`: `text-3xl font-extrabold text-white tracking-tight`
  - `Body Copy`: `text-sm text-slate-300 leading-relaxed`
  - `Caption / Subtext`: `text-xs text-slate-400`

---

## 3. Component Primitives Reference

### 3.1 `StatCard` (`src/components/ui/StatCard.jsx`)
- **Purpose:** Standardized KPI display widget for summary dashboards.
- **Props:** `title`, `value`, `subtitle`, `icon`, `trend`, `trendLabel`, `badge`, `progress`, `loading`.
- **Usage:** Used for Estimated Salary (P50), Salary Range (P10–P90), Matched Roles, and Roadmap Progress.

### 3.2 `ToastContext` & Toast Notification (`src/context/ToastContext.jsx`)
- **Purpose:** Global, accessible toast messaging system.
- **Usage:**
  ```jsx
  const { showSuccess, showError, showWarning, showInfo } = useToast();
  showSuccess('Salary prediction calculated successfully!');
  ```
- **Features:** Auto-dismissal (4000ms), manual close button, status icon, stacking order, accessibility role `alert`.

### 3.3 `EmptyState` (`src/components/ui/EmptyState.jsx`)
- **Purpose:** Graceful zero-data presentation with actionable next steps.
- **Props:** `icon`, `title`, `description`, `actionLabel`, `onAction`, `secondaryActionLabel`, `onSecondaryAction`.

### 3.4 `ErrorState` (`src/components/ui/ErrorState.jsx`)
- **Purpose:** Clear API error display with interactive retry capability.
- **Props:** `title`, `message`, `onRetry`, `retryLabel`.

### 3.5 `LoadingSkeleton` (`src/components/ui/LoadingSkeleton.jsx`)
- **Purpose:** Shimmer placeholders preventing layout shift during asynchronous data loading.
- **Variants:** `Skeleton`, `CardSkeleton`, `TableSkeleton`, `ChartSkeleton`.

### 3.6 `Modal` (`src/components/ui/Modal.jsx`)
- **Purpose:** Accessible modal dialog.
- **Features:** Focus trap, `Escape` key close listener, animated backdrop blur, size options (`sm`, `md`, `lg`, `xl`).

### 3.7 `ConfidenceIndicator` (`src/components/ui/ConfidenceIndicator.jsx`)
- **Purpose:** Visual progress meter and calibrated badge for ML prediction confidence.
- **Tiers:** High (>= 75%, Emerald), Moderate (50-74%, Amber), Low (< 50%, Rose).

### 3.8 `Breadcrumbs` (`src/components/ui/Breadcrumbs.jsx`)
- **Purpose:** Hierarchical navigation indicator in topbar reflecting current application route.

### 3.9 `SkillTagInput` (`src/components/ui/SkillTagInput.jsx`)
- **Purpose:** Interactive tag input for selecting, adding, and removing technical skills with auto-suggestions.

---

## 4. Application Layout & Navigation

### 4.1 Categorized Sidebar
The sidebar in `DashboardLayout.jsx` groups navigation into clear operational domains:
1. **Main:**
   - Overview (`/dashboard`)
   - Salary Valuation (`/salary-analysis`)
2. **Intelligence Engine:**
   - Explainability (SHAP) (`/explanations`)
   - Skill Intelligence (`/skill-intelligence`)
   - What-If Simulator (`/what-if`)
   - Role Matching (`/role-matching`)
   - Career Roadmaps (`/roadmaps`)
3. **Account & Settings:**
   - Saved Reports (`/reports`)
   - Profile Settings (`/settings`)

### 4.2 Topbar & Header
- Dynamic breadcrumb path display.
- Quick action CTA ("+ New Prediction").
- User profile summary pill with clickable logout dropdown.
- Mobile menu toggle button (hamburger icon).

---

## 5. Responsive Breakpoint Standards

- **Mobile (`< 640px` / `sm`):**
  - Navigation converts to slide-out drawer with dark backdrop overlay.
  - Multi-column grids collapse to single-column layout.
  - Large tables gain horizontal swipe scroll with sticky column headers.
  - Action buttons expand to full width for touch targets.
- **Tablet (`640px - 1024px` / `md`):**
  - Two-column dashboard KPI card layout.
  - Charts re-render dynamically with responsive SVG viewboxes.
- **Desktop (`>= 1024px` / `lg`):**
  - Persistent fixed-width sidebar (w-64).
  - 4-column KPI cards, side-by-side chart and shortlist panels.

---

## 6. Accessibility & Compliance (WCAG 2.1 AA)

1. **Color Contrast:** All body text meets minimum 4.5:1 contrast against `#020617` and `#0f172a`.
2. **Interactive States:** Visible keyboard focus outlines (`focus:ring-2 focus:ring-cyan-500 focus:outline-none`).
3. **Screen Readers:** ARIA labels on icon-only buttons (`aria-label="Toggle navigation"`, `aria-label="Close dialog"`).
4. **Semantics:** Proper document hierarchy (`<header>`, `<nav>`, `<main>`, `<aside>`, `<h1>`-`<h3>`).

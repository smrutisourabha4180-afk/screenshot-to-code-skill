# Screenshot-to-Code Workflow

Compact checklist form of the operating loop in `SKILL.md`.

## Phase 1 — Understand the reference

- [ ] Read the screenshot at the intended viewport
- [ ] Map page regions: nav, hero, sidebar, content, footer
- [ ] Identify the component tree and repeated elements
- [ ] Extract the type scale (family, size, weight, line height)
- [ ] Extract the palette, borders, radii, and shadows
- [ ] Inventory images, icons, and logos
- [ ] Note interactive and stateful regions
- [ ] Note responsive intent when multiple viewports are given
- [ ] List anything unreadable as an open question

## Phase 2 — Inspect the target project

- [ ] Detect framework and build system
- [ ] Detect package manager from the lockfile
- [ ] Locate entry points and routing
- [ ] Identify the styling system and design tokens
- [ ] List reusable components
- [ ] List existing assets and their directory convention
- [ ] Record the dev command

## Phase 3 — Plan

- [ ] Component boundaries
- [ ] Layout strategy (grid/flex, container widths, gutters)
- [ ] Breakpoints
- [ ] Required assets and how each is sourced
- [ ] New dependencies — justify each or drop it
- [ ] State and interaction requirements

## Phase 4 — Implement

- [ ] Build structure before styling
- [ ] Reuse existing components and tokens
- [ ] Keep changes inside the task's scope
- [ ] Avoid absolute positioning where flow layout works

## Phase 5 — Verify

- [ ] Start the dev server
- [ ] Render the page
- [ ] Capture at the reference viewport
- [ ] Diff against the reference
- [ ] Confirm no build or runtime errors

## Phase 6 — Refine

Fix in this order, largest deviation first:

1. Layout
2. Positioning
3. Dimensions
4. Spacing
5. Typography
6. Color
7. Images and icons
8. Borders and radius
9. Shadows
10. Micro-detail

Re-render after each round. Stop when remaining differences are cosmetic or explained.

## Phase 7 — Finish

- [ ] Application runs clean
- [ ] Target page verified against the reference
- [ ] Debug code removed
- [ ] Unrelated files untouched
- [ ] Deviations and verification tier reported

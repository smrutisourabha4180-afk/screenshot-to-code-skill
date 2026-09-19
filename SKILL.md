---

name: screenshot-to-code

description: Convert UI screenshots into accurate, production-ready frontend implementations. Use when a user provides a screenshot, mockup, reference image, or visual design and asks to recreate, reproduce, or convert it into code.

---

# Screenshot to Code

## Goal

Recreate the provided UI screenshot as accurately as practical in the user's existing project.

The result must be a working implementation, not merely a visual approximation or static mockup.

## Workflow

### 1. Inspect the project

Before changing code:

- Identify the framework and build system.
- Inspect the existing directory structure.
- Identify the entry points.
- Identify existing components and styling systems.
- Identify available assets.
- Reuse existing project infrastructure whenever possible.
- Do not replace the project's framework unnecessarily.

### 2. Analyze the reference

Study the screenshot carefully.

Identify:

- Overall page structure
- Header/navigation
- Main content areas
- Sidebar sections
- Cards
- Buttons
- Forms
- Images
- Icons
- Typography
- Font sizes
- Font weights
- Colors
- Borders
- Border radius
- Shadows
- Spacing
- Alignment
- Widths and heights
- Responsive behavior
- Visible states and interactions

Do not invent major UI elements that are not supported by the reference.

### 3. Plan the implementation

Before coding, determine:

- Component structure
- Layout strategy
- Responsive breakpoints
- Required assets
- Required dependencies
- State/interaction requirements

Prefer simple, maintainable components.

### 4. Implement

Build the UI in the project's existing technology stack.

Rules:

- Preserve existing project architecture.
- Reuse existing components when appropriate.
- Reuse existing assets when available.
- Do not introduce unnecessary dependencies.
- Do not rewrite unrelated files.
- Keep the implementation responsive.
- Match the reference's visual hierarchy closely.

### 5. Run the project

Start the development server using the project's existing commands.

Verify:

- The application starts successfully.
- There are no build errors.
- There are no obvious runtime errors.
- The recreated page is accessible.

### 6. Visual verification

Capture a screenshot of the implemented page.

Compare it against the reference.

Check:

- Layout
- Positioning
- Spacing
- Typography
- Colors
- Images
- Borders
- Shadows
- Component sizes
- Responsive behavior

### 7. Iterate

Fix the largest visual differences first.

Repeat:

render
↓
capture
↓
compare
↓
fix
↓
render again

Do not stop after the first implementation when visual verification is possible.

### 8. Finish

Before reporting completion:

- Verify the application builds/runs.
- Verify the target page works.
- Remove temporary debugging code.
- Keep changes limited to what the task requires.
- Summarize the files changed and the implementation.

## Visual Accuracy Rules

Prioritize visual accuracy in this order:

1. Overall layout
2. Component positioning
3. Dimensions and spacing
4. Typography
5. Colors
6. Images and icons
7. Borders and radius
8. Shadows and small details

Do not compensate for incorrect layout by adding unnecessary visual effects.

## Existing Assets

Always inspect the project for existing assets before creating replacements.

Prefer:

1. Existing project assets
2. User-provided assets
3. Appropriate local assets
4. Generated/recreated assets only when necessary

Do not use random placeholder images when the reference clearly contains a specific visual.

## Code Quality

The generated implementation must:

- Use semantic structure where practical.
- Follow the project's existing conventions.
- Avoid unnecessary duplication.
- Avoid unnecessary dependencies.
- Remain editable by another developer.
- Avoid hard-coded positioning when normal layout systems can reproduce the design.

## Important

The screenshot is the visual source of truth.

The existing project is the technical source of truth.

Do not destroy working project infrastructure merely to reproduce the screenshot.

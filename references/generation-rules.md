# Generation Rules

Distilled from `backend/prompts/system_prompt.py` in abi/screenshot-to-code. These are the constraints that make generated pages behave like real pages instead of static images. Apply them whenever generating a standalone prototype.

## Output discipline

- Be concise in chat. Do not paste code into messages; write files.
- For a brand-new page, write the full file once. For revisions, apply targeted edits — never regenerate the whole file.
- Keep a single primary artifact (`index.html` by default) unless the target project dictates otherwise.
- End with a one or two sentence summary of what was built.

## Assets: extract, do not imitate

- Extract real visual assets from the reference screenshot where possible (logos, product shots, photos, illustrations).
- If an asset cannot be extracted because it is occluded or is part of a background, generate a replacement — but never embed the whole screenshot as a page background. That defeats the purpose: the output must be coded, not an image.
- Use extracted assets for content imagery only. Never use them for layout, spacing, or structure.
- If an asset must render larger than its source resolution, upscale it rather than stretching it with CSS.
- Image generation and editing cannot produce transparency; remove backgrounds with a dedicated background-removal step instead.
- Batch independent image operations into one pass.

## Structural rules

- Prefer semantic HTML and normal flow layout.
- Keep the generated code editable by another developer: no generated spaghetti, no deeply nested absolute positioning.
- Reuse the target project's existing components, tokens, and assets before creating new ones.
- Respect the reference's responsiveness when more than one viewport is provided.

## Standalone stack scaffolding

Use these exact inclusions when producing a single-file prototype.

**Tailwind (HTML, React, Vue, Ionic)**

```html
<script src="https://cdn.tailwindcss.com"></script>
```

**HTML + CSS** — plain HTML, CSS, and JS only. Do not add Tailwind.

**Bootstrap**

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
```

**React (in-browser)**

```html
<script src="https://cdn.jsdelivr.net/npm/react@18.0.0/umd/react.development.js"></script>
<script src="https://cdn.jsdelivr.net/npm/react-dom@18.0.0/umd/react-dom.development.js"></script>
<script src="https://unpkg.com/@babel/standalone@7.25.6/babel.min.js"></script>
```

Pin Babel to `7.25.6` exactly. The unversioned URL now resolves to Babel 8, whose automatic JSX runtime injects an `import` that breaks in-browser transforms. Do not use `cdn.babeljs.io/babel.min.js`.

**Ionic**

```html
<script type="module" src="https://cdn.jsdelivr.net/npm/@ionic/core/dist/ionic/ionic.esm.js"></script>
<script nomodule src="https://cdn.jsdelivr.net/npm/@ionic/core/dist/ionic/ionic.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@ionic/core/css/ionic.bundle.css" />
```

Ionic icons:

```html
<script type="module">
  import ionicons from 'https://cdn.jsdelivr.net/npm/ionicons/+esm'
</script>
<script nomodule src="https://cdn.jsdelivr.net/npm/ionicons/dist/esm/ionicons.min.js"></script>
<link href="https://cdn.jsdelivr.net/npm/ionicons/dist/collection/components/icon/icon.min.css" rel="stylesheet">
```

**Vue (global build)**

```html
<script src="https://registry.npmmirror.com/vue/3.3.11/files/dist/vue.global.js"></script>
```

```html
<div id="app">{{ message }}</div>
<script>
  const { createApp, ref } = Vue
  createApp({
    setup() {
      const message = ref('Hello vue!')
      return { message }
    }
  }).mount('#app')
</script>
```

**Fonts and icons (all stacks)**

- Google Fonts or other publicly accessible fonts are allowed.
- Except for Ionic, use Font Awesome for icons:

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
```

## Revising a specific element

When the user scopes a change to one element, the captured `outerHTML` is a locator, not source: it comes from the live DOM, so it may differ from the file (JSX uses `className`, Vue templates use directives and interpolations, Ionic and Bootstrap inject classes at runtime).

Recover the source that produces that element by matching tag, classes, ids, and text content, then change only that element and its rendering logic. Leave the rest of the file untouched.

## Anti-patterns

- Embedding the reference screenshot as the page.
- Placeholder image services when the reference shows a specific visual.
- Absolute positioning where grid or flex works.
- Regenerating an entire file to change one class.
- Adding dependencies the project already solves internally.
- Declaring completion without rendering the page.

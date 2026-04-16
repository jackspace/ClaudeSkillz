---
name: fluxwing-library-browser
description: "Browse and view all available uxscii components including bundled templates, user components, and screens. Use when working with .uxm files, when user wants to see, list, browse, or search .uxm components or screens."
version: 0.0.1
author: Trabian
allowed-tools: Read, Glob, Grep
---

# Fluxwing Library Browser

Browse all available uxscii components: bundled templates, user-created components, and complete screens.

## Data Location Rules

**READ from (bundled templates - reference only):**
- `{SKILL_ROOT}/../uxscii-component-creator/templates/` - 11 component templates
- `{SKILL_ROOT}/../uxscii-screen-scaffolder/templates/` - 2 screen examples (if available)
- `{SKILL_ROOT}/docs/` - Documentation

**READ from (project workspace):**
- `./fluxwing/components/` - Your created components
- `./fluxwing/screens/` - Your created screens
- `./fluxwing/library/` - Customized template copies

**NEVER write to skill directories - they are read-only!**

## Your Task

Show the user what uxscii components are available across **four sources**:
1. **Bundled Templates** - 11 curated examples from skill templates (read-only reference)
2. **Project Components** - User/agent-created reusable components in `./fluxwing/components/` (editable)
3. **Project Library** - Customized template copies in `./fluxwing/library/` (editable)
4. **Project Screens** - Complete screen compositions in `./fluxwing/screens/` (editable)

**Key Distinction**: Bundled templates are READ-ONLY reference materials. To customize them, copy to your project workspace first.

## Fast Browsing with Pre-Built Index

**IMPORTANT**: Use the pre-built template index for instant browsing instead of globbing individual files.

Use the `Read` tool to load the index:

```
Read {SKILL_ROOT}/data/template-index.json
```

The index provides:
- `bundled_templates[]` - Array of component metadata (id, name, description, preview, states, props, tags)
- `by_type` - Components grouped by type (button, input, card, modal, etc.)
- `by_tag` - Components grouped by tags (form, interactive, navigation, etc.)

**Index structure:**
```json
{
  "version": "1.0.0",
  "generated": "2025-10-18T12:00:00Z",
  "template_count": 11,
  "bundled_templates": [{ "id": "primary-button", "name": "Primary Button", "description": "...", "preview": "...", "states": [], "props": [], "tags": [] }],
  "by_type": { "button": ["primary-button", "icon-button"] },
  "by_tag": { "form": ["text-input", "email-input"] }
}
```

**When to use full file reads instead:**
- User requests detailed view of a specific component (need full `.uxm` content)
- User wants to copy a template (need both `.uxm` and `.md` files)
- Searching for a property not present in the index

## Display Format

Present results in a hierarchical tree grouped by source. Show component name, description, and an inline ASCII preview where available. Use the pre-built index previews for bundled templates.

**Abbreviated example:**
```
BUNDLED TEMPLATES (11)
  Buttons (2): primary-button.uxm, icon-button.uxm
  Inputs (2): text-input.uxm, email-input.uxm
  Cards (1): card.uxm
  ...

YOUR COMPONENTS (./fluxwing/components/)
  submit-button.uxm - Custom submit button for forms

YOUR SCREENS (./fluxwing/screens/)
  login-screen.uxm - Components: email-input, password-input, submit-button

Total: 11 templates, 1 component, 1 screen
```

For the full display format with ASCII previews, see `{SKILL_ROOT}/DISPLAY_REFERENCE.md`.

## Supported Actions

After browsing, support these user actions:

- **View details**: Read the full `.uxm` file and show metadata, props, states, accessibility info, and ASCII preview
- **Copy template**: Copy `.uxm` and `.md` from bundled templates to `./fluxwing/library/`, then verify the copied files exist with `Read`
- **Search**: Use `Glob` and `Grep` across all four sources to find components by name, type, or pattern
- **Create**: Direct user to the Component Creator skill for new components
- **Scaffold**: Direct user to the Screen Scaffolder skill for new screens

When no project components or screens exist yet, indicate this clearly and suggest creation commands.

## Resources

- **Display Reference**: See `{SKILL_ROOT}/DISPLAY_REFERENCE.md` for detailed output format templates
- **Examples Guide**: See `{SKILL_ROOT}/docs/07-examples-guide.md` for detailed template documentation
- **Component Creator**: Use when you want to create new components
- **Screen Scaffolder**: Use when you want to build complete screens
- **Component Viewer**: Use for detailed component information

## Important Notes

1. **Read-only templates**: Bundled templates cannot be modified directly
2. **Copy before customize**: Copy templates to `./fluxwing/library/` to customize
3. **Verify after copy**: Always confirm copied files are readable before reporting success
4. **Search**: Use Glob and Grep to find components by name or pattern
5. **Organization**: Keep components in `./fluxwing/components/`, customized templates in `./fluxwing/library/`
6. **Screens**: Screen files include `.uxm`, `.md`, and `.rendered.md` (three files)

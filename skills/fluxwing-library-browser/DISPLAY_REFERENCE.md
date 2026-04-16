# Fluxwing Library Browser - Display Reference

This file contains detailed display format templates for the library browser output.
The main SKILL.md contains the core logic; refer here for full formatting examples.

## Full Browse Output Format

Present in a clear, hierarchical structure, grouped by source:

```
BUNDLED TEMPLATES
Component Creator Templates
-----------------------------------------------------
These are starter templates you can copy and customize.

Buttons (2 variants)
  +- primary-button.uxm
  |  +-- Standard clickable button with hover, focus, and disabled states
  |     [  Click Me  ]
  |
  +- icon-button.uxm
     +-- Button with icon support for visual emphasis
        [Search]

Inputs (2 variants)
  +- text-input.uxm
  |  +-- Basic text input with validation states
  |     [________________]
  |
  +- email-input.uxm
     +-- Email-specific input with format validation
        [user@example.com  ]

Cards (1 variant)
  +- card.uxm
     +-- Container for grouping related content

Modals (1 variant)
  +- modal.uxm
     +-- Overlay dialog for focused interactions

Navigation (1 variant)
  +- navigation.uxm
     +-- Primary navigation menu

Feedback (2 variants)
  +- alert.uxm
  |  +-- User notification with severity levels
  |
  +- badge.uxm
     +-- Small status indicator or label

Lists (1 variant)
  +- list.uxm
     +-- Vertical list for displaying data

-----------------------------------------------------

YOUR COMPONENTS
./fluxwing/components/
-----------------------------------------------------
Components you've created for your project.

  submit-button.uxm
  +-- Custom submit button for forms
     Modified: 2024-10-11 14:23:00

  password-input.uxm
  +-- Password input with show/hide toggle
     Modified: 2024-10-11 14:25:00

-----------------------------------------------------

YOUR SCREENS
./fluxwing/screens/
-----------------------------------------------------
Complete screen compositions.

  login-screen.uxm
  +-- User authentication screen
     Components used: email-input, password-input, submit-button, error-alert

  dashboard.uxm
  +-- Main application dashboard
     Components used: navigation, metric-card, data-table, sidebar

-----------------------------------------------------
Total: 11 templates, 2 components, 2 screens
```

## Detailed Component View

When a user asks for details on a specific component, show metadata from the index
and read the full `.uxm` file only for this view:

```
PRIMARY-BUTTON.UXM
-----------------------------------------------------
ID: primary-button
Type: button
Version: 1.0.0
Description: Standard clickable button with hover, focus, and disabled states

Props:
  - text: "Click me"
  - variant: "primary"
  - disabled: false

States:
  - default (solid border, white background)
  - hover (highlighted background)
  - focus (outline indicator)
  - disabled (grayed out)

Accessibility:
  - Role: button
  - Focusable: true
  - Keyboard: Space, Enter

ASCII Preview (from .uxm):
  [default]    [hover]
  Click Me     Click Me

Location: {SKILL_ROOT}/../uxscii-component-creator/templates/primary-button.uxm
To customize: Copy to ./fluxwing/library/ for editing
```

## Copy Template Flow

```
User: Copy primary-button to my project

Agent:
1. Read source files from {SKILL_ROOT}/../uxscii-component-creator/templates/
2. Write .uxm and .md to ./fluxwing/library/primary-button.*
3. Verify copied files exist and are readable

Output:
  Copied to ./fluxwing/library/
    - primary-button.uxm
    - primary-button.md

  Next steps:
  - Edit: Modify ./fluxwing/library/primary-button.uxm
  - Expand: "add hover state to primary-button"
  - Use: Reference it in screens or other components
```

## Search Results Format

```
User: Find all button components

Found 3 button components:

Bundled Templates:
  - primary-button.uxm (standard clickable button)
  - icon-button.uxm (button with icon support)

Your Components:
  - submit-button.uxm (custom submit button for forms)
```

## Empty Library Output

When the user has no project components or screens yet:

```
BUNDLED TEMPLATES
  11 starter templates available (use browse to see all)

YOUR COMPONENTS (./fluxwing/components/)
  No components yet.
  Try: "Create a submit button" or "Create an email input"

YOUR SCREENS (./fluxwing/screens/)
  No screens yet.
  Try: "Build a login screen" or "Create a dashboard"

Total: 11 templates, 0 components, 0 screens
```

---
name: check-dod-compliance
description: Checks branch changes against the Definition of Done (DoD) checklist and generates a detailed compliance report.
---

# Check Definition of Done (DoD) Compliance

This skill helps you automatically analyze changes on your current git branch against the team's Definition of Done (DoD) rules and generate a structured compliance report.

## How to Execute the Skill

Follow these steps to perform the compliance check:

### Step 1: Gather Git Diffs and Changed Files
Run the following helper script in the workspace root directory to list the modified files and determine their category (Frontend vs. Backend/Other):

```bash
python .gemini/skills/check-dod-compliance/scripts/get_diff.py
```

*Note: You can pass `--base <branch_name>` if you wish to compare against a branch other than the automatically detected default (such as `origin/develop` or `origin/master`).*

### Step 2: Perform the Code Analysis
> [!IMPORTANT]
> **Constraint:** You must ONLY analyze, evaluate, and report on files/lines that are part of the current branch's changes (as listed by the `get_diff.py` script). Do NOT inspect, analyze, flag violations, or report on unmodified files or pre-existing code in the repository.

For each changed or added file identified by the script, read the file contents using `view_file` or run targeted grep searches. Evaluate them against the respective sections of the DoD checklist below.


---

## The Definition of Done (DoD) Checklist

### General MR Checklist
Apply these checks to the entire change set:
- **[ ] Merged Base Branch**: Ensure you have pulled and merged the base branch (usually `master` or `develop`) into your feature branch. Check if the git log shows a merge commit or if local commits are up-to-date.
- **[ ] Self-Review**: Perform a mental self-review of logic correctness.
- **[ ] Code Formatting**: Ensure code adheres to local formatting standards (check for consistent indentation, quotes, etc.).
- **[ ] Complete Feature**: Verify that the feature is fully finished and not left with placeholders or unfinished TODOs.
- **[ ] Correct Target Branch**: Confirm that this MR targets the `develop`/`developer` branch.
- **[ ] Clean Code**: Check that all debug code, temporary comments, and `console.log` statements have been removed.
- **[ ] Wiki Documentation**: Check if the change requires a wiki or documentation update, and if so, that one has been created/queued.
- **[ ] Test Coverage**: If it is a core feature, ensure thorough tests (unit, integration, or e2e) are added.
- **[ ] Passing Tests**: Ensure all added and existing tests are passing.

---

### Frontend Specific Checklist
Apply these checks to any added or modified frontend files (`.tsx`, `.ts`, `.jsx`, `.js`, `.css`, `.scss`, `.html`):

#### 1. Perceivable
- **[ ] Media Subtitles**: Check if any audio or video tags have corresponding `<track>` tags or text fallback for subtitles.
- **[ ] Reduced Motion**: Verify that any animations (transitions, keyframes) respect the `prefers-reduced-motion` media query in CSS or JS.
- **[ ] Visible Input Labels**: Ensure all `<input>`, `<select>`, and `<textarea>` fields have associated visible `<label>` tags (using `htmlFor` or nested hierarchy). Avoid relying solely on placeholders.

#### 2. Layout and Information Hierarchy
- **[ ] Layout Responsiveness**: Verify responsive styles (e.g. flexbox, grid, media queries).
- **[ ] Zoom Usability**: Check that layouts are flexible and use relative units (`em`, `rem`, `%`, `vh`, `vw`) rather than fixed pixels so that content remains usable at 200% and 400% zoom (WCAG 1.4.4).
- **[ ] No Horizontal Scroll**: Ensure layouts do not cause horizontal scrolling at a viewport width of 320 CSS pixels (WCAG 1.4.10).
- **[ ] Touch Targets**: Check that interactive elements (buttons, links, form inputs) are at least 44×44px in size, or have sufficient spacing around them (WCAG 2.5.8).
- **[ ] Primary Purpose & Visual Hierarchy**: Check that each page or section has a single primary focus, and font sizes/weights support the semantic hierarchy.
- **[ ] Spacing and Grouping**: Ensure margins, paddings, and border boxes are used consistently to group related items and aid visual orientation.

#### 3. Colors
- **[ ] Color Contrast**: Verify that text-to-background contrast ratio is at least 4.5:1 (or 3:1 for large text) and interactive UI elements have a 3:1 contrast ratio.
- **[ ] Color as Sole Carrier**: Ensure no instructions, statuses, or alerts rely purely on color. (e.g., if a field turns red on error, there must also be a textual error message or an error icon).

#### 4. Fonts / Text
- **[ ] Font Family**: Check that the CSS uses sans-serif fonts as the base (e.g., `font-family: sans-serif`, or system sans-serif families).
- **[ ] Distinguishability**: Ensure character legibility. Avoid highly decorative or condensed fonts.
- **[ ] Not Italic by Default**: Verify body text is not italic (italics should only be used for emphasis on specific words).
- **[ ] No Long Texts in All-Caps**: Check that paragraphs or long sentences do not use uppercase (e.g. `text-transform: uppercase` or typed all-caps).
- **[ ] Text Alignment**: Ensure long blocks of text are left-aligned (not justified or centered) for readability.
- **[ ] Semantic Emphasis**: Confirm that bold/italic styling is used deliberately and sparingly.
- **[ ] Descriptive Hyperlinks**: Verify link text itself describes the destination (e.g. use "Read the API documentation" instead of "click here" or "link").
- **[ ] Fluid Reading**: Ensure line height is adequate (usually 1.5 for body text) and font sizes are legible.

#### 5. Images
- **[ ] Meaningful Alt Text**: Verify all `<img>` or Next.js `<Image>` tags have descriptive `alt` text. For purely decorative images, use `alt=""`.
- **[ ] Appropriate Fallbacks**: Ensure image loaders or placeholders are implemented in case of loading failures.

#### 6. Operable
- **[ ] Keyboard Accessibility**: Ensure all clickable actions can be triggered via keyboard (using spacebar or Enter key). Interactive elements must use focusable HTML tags (`<button>`, `<a>`, `<input>`) or have a `tabIndex={0}` with appropriate key event handlers.
- **[ ] Focus Order**: Verify that keyboard tab navigation follows the visual layout structure (top-to-bottom, left-to-right).
- **[ ] No Keyboard Traps**: Ensure focus does not get trapped within modals, dropdowns, or calendars without an easy keyboard exit (like the Esc key).
- **[ ] Skip Links and Landmarks**: Verify HTML5 landmark tags (`<header>`, `<nav>`, `<main>`, `<footer>`, `<aside>`) are present.
- **[ ] Visible Focus Indicator**: Confirm all interactive elements show a clear focus outline/indicator when focused. The focus indicator must be at least 2px wide and have a contrast ratio of at least 3:1 against the background (WCAG 2.4.13).
- **[ ] Time Limits**: Verify there are no unnecessary automatic page redirects or strict session timeouts.

#### 7. Understandable
- **[ ] Language**: Check that clear, plain language is used.
- **[ ] Heading Hierarchy**: Verify heading levels (`<h1>`, `<h2>`, `<h3>`, etc.) are nested sequentially without skipping levels.
- **[ ] Form Field Labels**: Avoid placeholders as replacements for visible labels.
- **[ ] Consistent Behavior**: Ensure standard visual patterns and interaction flows are consistent across pages.
- **[ ] Precise Error Messages**: Confirm form validation displays helpful, specific messages with resolution hints.
- **[ ] Error Location & Highlights**: Check that error text is placed adjacent to the invalid input field and visually highlighted.
- **[ ] Error Summaries**: When multiple validation errors occur in a single form, ensure there is an error summary box at the top of the form with anchor links linking to the specific invalid fields.
- **[ ] Screen Reader Announcements**: Verify dynamic content or statuses (e.g. loading, success, error) are announced to screen readers using ARIA live regions (`aria-live="polite"` or `role="alert"` / `role="status"`).
- **[ ] Subtle Live Validation**: Live validation error messages should not show up prematurely (e.g., do not show an error on a field while the user is still typing, show it on blur or on submit).

#### 8. Robust
- **[ ] Semantic Elements**: Ensure correct use of elements like `<form>`, `<button>`, `<a>`, `<nav>`, `<section>`, instead of styled `<div>` elements.

---

### Step 3: Write the Compliance Report
Upon completing the analysis, create a markdown file named `dod_compliance_report.md` in the repository's root or workspace directory. Use the following structured format:

````markdown
# Definition of Done (DoD) Compliance Report

**Branch:** [branch-name]
**Compare Base:** [target-branch]
**Analysis Date:** [date]

## 📊 Summary
| Category | Passed | Failed | N/A | Total |
|---|---|---|---|---|
| General MR | [count] | [count] | [count] | [count] |
| Frontend | [count] | [count] | [count] | [count] |
| **Total** | **[count]** | **[count]** | **[count]** | **[count]** |

---

## 🔍 Detailed Checklist Analysis

### General MR Checklist
- [ ] **Merged Base Branch**: [Status: Pass/Fail/NA] - [Brief explanation or file trace]
- [ ] **Self-Review**: [Status: Pass/Fail/NA] - [Brief explanation]
...

### Frontend Specific Checklist
*(Only include if frontend files are modified)*

#### 1. Perceivable
- [ ] **Media Subtitles**: [Status] - [Explanation]
- [ ] **Reduced Motion**: [Status] - [Explanation]
...

---

## 🚨 Violations & Action Items
List any items marked as `Fail` with precise details:
1. **[File Name] (Line [Number])**: [DoD Criteria]
   - *Issue:* [What failed?]
   - *Fix:* [How to resolve it?]
   - *Example link:* [filename.tsx:L12-15](file:///...)
2. ...
````

### Step 4: Present Findings
Report a high-level summary of the findings in the chat interface, and point the user to the generated `dod_compliance_report.md` file for full details and inline links.

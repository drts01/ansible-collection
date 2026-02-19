---
description: 'Documentation and content creation standards'
applyTo: '**/docs/**/*.md,**/README.md'
---

# Documentation Instructions

## Goals
- Provide accurate, actionable guidance for engineers and stakeholders.
- Maintain consistent voice, formatting, and terminology.
- Ensure documentation can be validated automatically where possible.

## Authoring Checklist
- Prefer numbered steps for procedures; use tables only for structured data.
- Write in present tense, second person (“You”) and keep sentences ≤25 words.
- Use code fences with language tags; add inline comments when needed.

## Formatting Rules
- Wrap lines at 100 characters.
- Use sentence case for headings.
- Link to internal pages with relative paths, external sources with HTTPS URLs.
- Embed images with descriptive alt text and store them under `docs/assets/`.

## README Guidelines
- The root `README.md` must summarize the product, architecture overview, quick start, and support channels.
- Each significant module may include a scoped `README.md` with Purpose → Setup → Usage → Troubleshooting.
- Keep status badges current; link to detailed docs rather than duplicating content.
- Update READMEs whenever configuration, scripts, or onboarding steps change and reference the related ticket.

## Tooling
- Author and build static docs with **Hugo** or **MkDocs**; keep configs under `docs/site/` and document custom themes.
- Create architecture or flow diagrams with **Mermaid**; embed diagrams inline using ```mermaid code fences.

## Review Expectations
- Open a PR labeled `docs`.
- Include a checklist confirming lint, links, and diagrams were updated.
- Request review from `@uhg/docs-maintainers`.
- Address feedback within two business days and keep discussion in-thread.

## Versioning & Changelog
- Note documentation-only changes under a dedicated “Docs” section in `CHANGELOG.md`.
- When documenting new features, reference the feature flag or release ID.

## Archival
- For deprecated pages, add a banner at the top linking to the replacement.
- Move outdated files to `docs/archive/` with a date-stamped filename.

## Markdown Content Rules

The following markdown content rules are enforced in the validators:

1. **Headings**: Use appropriate heading levels (H2, H3, etc.) to structure your content. Do not use an H1 heading, as this will be generated based on the title.
2. **Lists**: Use bullet points or numbered lists for lists. Ensure proper indentation and spacing.
3. **Code Blocks**: Use fenced code blocks for code snippets. Specify the language for syntax highlighting.
4. **Links**: Use proper markdown syntax for links. Ensure that links are valid and accessible.
5. **Images**: Use proper markdown syntax for images. Include alt text for accessibility.
6. **Tables**: Use markdown tables for tabular data. Ensure proper formatting and alignment.
7. **Line Length**: Limit line length to 400 characters for readability.
8. **Whitespace**: Use appropriate whitespace to separate sections and improve readability.
9. **Front Matter**: Include YAML front matter at the beginning of the file with required metadata fields.

## Formatting and Structure

Follow these guidelines for formatting and structuring your markdown content:

- **Headings**: Use `##` for H2 and `###` for H3. Ensure that headings are used in a hierarchical manner. Recommend restructuring if content includes H4, and more strongly recommend for H5.
- **Lists**: Use `-` for bullet points and `1.` for numbered lists. Indent nested lists with two spaces.
- **Code Blocks**: Use triple backticks (`) to create fenced code blocks. Specify the language after the opening backticks for syntax highlighting (e.g., `csharp).
- **Links**: Use `[link text](URL)` for links. Ensure that the link text is descriptive and the URL is valid.
- **Images**: Use `![alt text](image URL)` for images. Include a brief description of the image in the alt text.
- **Tables**: Use `|` to create tables. Ensure that columns are properly aligned and headers are included.
- **Line Length**: Break lines at 80 characters to improve readability. Use soft line breaks for long paragraphs.
- **Whitespace**: Use blank lines to separate sections and improve readability. Avoid excessive whitespace.

## Validation Requirements

- **Content Rules**: Ensure that the content follows the markdown content rules specified above.
- **Formatting**: Ensure that the content is properly formatted and structured according to the guidelines.
- **Validation**: Run the validation tools to check for compliance with the rules and guidelines.

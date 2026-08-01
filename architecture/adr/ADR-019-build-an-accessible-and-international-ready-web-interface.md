# ADR-019: Build an Accessible and International-Ready Web Interface

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owners:** POLARIS maintainers

## Context

POLARIS is intended to demonstrate software for government, regulatory, research, and international-organisation users. Accessibility is therefore a product requirement and a prerequisite for a credible public portfolio deployment. It is substantially more expensive to repair after custom interaction patterns and design primitives have spread through the application.

The initial user interface may be English-only, but the product must preserve and analyse evidence in multiple languages. Encoding, language metadata, time handling, and translatable interface structure are similarly expensive to retrofit after data and presentation contracts have stabilized.

## Decision

Target WCAG 2.2 Level AA for every user-facing page and complete user journey.

Build the interface from a small set of reusable accessible primitives. Require:

- semantic HTML before ARIA;
- native controls unless a custom interaction has a demonstrated need;
- complete keyboard operation with visible, logical focus;
- correct focus placement and restoration across navigation, dialogs, errors, and asynchronous updates;
- accessible authentication and form validation;
- programmatically determinable names, roles, states, relationships, and status messages;
- sufficient text and non-text contrast;
- support for zoom, reflow, reduced motion, and minimum target sizes;
- alternatives to dragging, complex gestures, and pointer-only operation;
- no information communicated by color, position, or motion alone.

Use React Aria Components as the behavior and accessibility layer for non-native composite controls. Wrap only the components required by implemented user journeys in a small application-owned `packages/ui` package. Use semantic native elements directly where they are sufficient.

Style the POLARIS layer with a small set of CSS custom-property tokens and locally owned styles. Government design systems such as GOV.UK and the UK Home Office design system are pattern references for clear language, forms, validation, task flows, and accessibility; POLARIS does not copy their branding or import a complete government theme.

Document processing and AI workflows must announce upload progress, processing state, errors, completed results, and material content changes without unexpectedly moving keyboard focus. Document navigation, evidence citations, and issue matrices must remain usable with a keyboard and screen reader.

Accessibility verification includes:

- automated checks in component and page tests;
- keyboard checks for each critical journey;
- focus-order and focus-restoration tests;
- manual testing with at least one supported screen reader before the public portfolio release;
- human review of interactions that automated tools cannot evaluate.

Automated tools support but do not establish conformance. A formal accessibility claim requires a dedicated conformance assessment.

Prepare for international use from the first implementation:

- use UTF-8 in the browser, API, database, files, and generated artifacts;
- identify source, evidence, and generated-content languages with BCP 47 language tags;
- store instants in UTC and format dates, times, numbers, and currencies in the presentation layer;
- accept Unicode names, organizations, jurisdictions, and document content without locale-specific structural assumptions;
- store initial English interface text in a message catalogue rather than distributing it through components;
- avoid constructing sentences by concatenating translated fragments;
- set document language and direction metadata correctly;
- prefer CSS logical properties so right-to-left support does not require a new layout architecture.

The MVP may ship with one interface language. Translation, right-to-left release certification, WCAG Level AAA, and jurisdiction-specific procurement reports are not required until a corresponding product or contractual need exists.

## Consequences

### Positive

- Accessibility is built into shared primitives instead of repeatedly repaired in features.
- Critical policy workflows remain available to keyboard and assistive-technology users.
- The project has a clear, testable conformance target.
- Multilingual evidence is preserved correctly from the beginning.
- Adding a second interface language does not require first extracting all presentation text.
- Native controls and shared primitives reduce implementation and testing cost.
- React Aria supplies difficult interaction behavior without imposing visual branding.

### Negative

- UI work requires deliberate focus, keyboard, and announcement behavior.
- Some otherwise attractive third-party components will be unsuitable.
- Manual accessibility verification remains necessary.
- Message-catalogue and locale abstractions add modest overhead before translation is needed.
- Formal procurement conformance may still require external assessment.
- Wrapped components still require POLARIS-specific styling and end-to-end accessibility verification.

## Rejected Alternatives

- **Remediate accessibility after the MVP:** allows inaccessible primitives and interaction patterns to become systemic.
- **Rely only on automated accessibility scanning:** cannot verify usability, reading order, focus behavior, or appropriate announcements.
- **Target WCAG Level AAA for the entire application:** creates disproportionate constraints and is not a generally suitable whole-site target.
- **Build a custom design system from scratch:** adds substantial work when accessible native elements and established primitives can be composed.
- **Adopt a complete branded government design system:** imports another service's visual identity and a larger component surface than the portfolio application needs.
- **Use an unstyled headless primitive library without a consistent accessibility baseline:** shifts more keyboard, focus, and internationalization responsibility to one maintainer.
- **Hard-code English until translation is requested:** makes later localization an expensive cross-application rewrite.
- **Translate the MVP immediately:** adds product and verification scope without a selected second locale.

## Review Triggers

Review this decision when:

- procurement requires EN 301 549, Section 508, or another jurisdictional standard;
- a formal accessibility conformance report is required;
- a second interface locale is approved;
- right-to-left interface support becomes a release requirement;
- user research identifies needs beyond the WCAG 2.2 Level AA baseline;
- React Aria no longer supports the required React or Next.js version;
- the local UI package grows beyond roughly twenty maintained composite components or needs independent consumers.

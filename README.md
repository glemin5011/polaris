# Policy Analysis, Research and Intelligence System (POLARIS)

POLARIS is an open-source, AI-assisted workbench for public-policy analysis. It helps policy teams organise evidence, model stakeholder perspectives, review policy proposals, prepare consultations and preserve the reasoning behind policy decisions.

## 1. Core Problem

Public-policy teams commonly work with fragmented information:

- policy documents;
- previous consultation submissions;
- meeting notes;
- stakeholder CRM records;
- research papers;
- ministerial priorities;
- legal opinions;
- impact assessments;
- institutional positions;
- historical decisions.

This information is often distributed across document repositories, email, spreadsheets and individual officials’ institutional memory that is lost when they leave or retire.

As a result:

- important stakeholder objections are discovered late;
- evidence is difficult to trace;
- officials repeat previous analysis;
- policy assumptions are insufficiently challenged;
- new team members lack historical context;
- consultation questions are too broad;
- decisions cannot later be reconstructed;
- the loudest or best-documented stakeholders receive disproportionate attention.

POLARIS should provide a structured workspace that connects policy design, evidence, stakeholders, simulations, consultation preparation and decisions.

## 2. Product Vision

POLARIS should become an evidence-grounded operating system for policy development.

A policymaker should be able to create a policy case, upload relevant documents, register affected stakeholders, draft or import a policy proposal and ask POLARIS to identify:

- likely stakeholder objections;
- areas of support or conditional support;
- conflicts between stakeholder interests;
- implementation risks;
- missing evidence;
- unsupported assumptions;
- underrepresented stakeholder groups;
- questions that should be tested during consultation;
- policy clauses that may require revision.

The system should help policymakers prepare for real consultation. It does not replace real-life consultation or perfectly predict stakeholder behaviour.

The central product proposition is:

> POLARIS turns policy documents, institutional evidence and stakeholder intelligence into traceable consultation preparation, issue analysis and decision memory.

## 3. Target Users

The primary users are:

- national government policy officials;
- international organisations such as the OECD, European Commission, World Bank and United Nations;
- regulatory authorities;
- legislative research services;
- public-sector economists;
- policy analysts;
- consultation teams;
- think tanks;
- civil-society policy teams;
- academic policy researchers.

The initial product is designed primarily for an experienced policy team working on complex international or regulatory policy.

## 4. Primary Use Case

A policymaker creates a policy case and adds:

- the policy problem;
- objectives;
- constraints;
- proposed policy options;
- a draft policy document;
- supporting research;
- previous consultation submissions;
- stakeholder profiles;
- historical statements and positions.

The policymaker then runs a **consultation rehearsal**.

POLARIS reviews the proposal from the perspective of selected stakeholders and produces an evidence-grounded issue matrix containing:

- affected clause;
- stakeholder;
- likely position;
- rationale;
- requested change;
- relevant evidence;
- confidence;
- whether the position was observed or inferred;
- unsupported assumptions;
- recommended consultation questions.

The policymaker revises the document and runs another review. POLARIS shows which concerns were resolved, which remain and which were introduced by the revision.

## 5. Product Principles

### 5.1 Evidence before persona

Stakeholder agents must be created from attributable evidence, not generic stereotypes (if data is available).

Relevant evidence may include:

- previous consultation submissions;
- public statements;
- organisational mandates;
- meeting notes;
- policy papers;
- parliamentary testimony;
- official correspondence;
- jurisdictional constraints;
- historical voting or negotiation positions.

A prompt such as “act like a multinational company” is not sufficiently reliable. Such vague agents may provide limited value when data about real stakeholders is not available.

### 5.2 Observed and inferred positions must remain separate

Every stakeholder position must be classified as:

- **Observed** — explicitly supported by evidence.
- **Inferred** — derived from evidence but not directly stated.
- **Mixed** — contains both observed and inferred elements.
- **Unsupported** — not adequately supported and therefore flagged.

The UI and data model must never blur this distinction.

### 5.3 Simulations generate hypotheses

POLARIS should say:

> Based on the available evidence, this stakeholder may raise the following concern.

It should not say:

> This stakeholder will oppose the proposal.

Synthetic stakeholder agents are tools for preparation, not authoritative predictions of how real stakeholders will react to the given problem.

### 5.4 Consultation cannot be replaced

POLARIS must never present agent simulations as a substitute for:

- public consultation;
- stakeholder interviews;
- expert review;
- parliamentary scrutiny;
- legal analysis;
- economic modelling;
- democratic decision-making.

### 5.5 Every conclusion must be traceable

Material claims should contain:

- source citations;
- retrieved passages;
- evidence dates;
- stakeholder-profile version;
- policy-document version;
- prompt version;
- model configuration;
- confidence;
- human review status.

### 5.6 Reproducibility matters

Each simulation run should preserve:

- the exact policy version;
- the evidence snapshot;
- the stakeholder profiles used;
- the retrieved evidence;
- the model and provider;
- model parameters;
- prompt versions;
- structured outputs;
- validation failures;
- human edits.

### 5.7 Independent analysis before synthesis

Synthetic stakeholders should initially review a proposal independently.

One generated stakeholder response must not influence another stakeholder’s initial response. A synthesis stage may compare the independent reviews afterward.

### 5.8 Agent counts are not public opinion

The number of synthetic agents supporting or opposing a policy has no statistical meaning.

POLARIS must not convert simulated responses into percentages representing public opinion.

### 5.9 Missing voices must be visible

The system should identify groups that may be affected but are missing or weakly represented in the evidence.

This includes stakeholders that:

- publish fewer documents;
- operate in less digitised jurisdictions;
- use languages poorly represented by the model;
- have limited institutional capacity;
- are affected indirectly;
- implement the policy rather than negotiate it.

### 5.10 Humans remain accountable

The system may produce recommendations, but policy decisions must remain human decisions.

---

# Turborepo starter

This Turborepo starter is maintained by the Turborepo core team.

## Using this example

Run the following command:

```sh
npx create-turbo@latest
```

## What's inside?

This Turborepo includes the following packages/apps:

### Apps and Packages

- `docs`: a [Next.js](https://nextjs.org/) app
- `web`: another [Next.js](https://nextjs.org/) app
- `@repo/ui`: a stub React component library shared by both `web` and `docs` applications
- `@repo/eslint-config`: `eslint` configurations (includes `eslint-config-next` and `eslint-config-prettier`)
- `@repo/typescript-config`: `tsconfig.json`s used throughout the monorepo

Each package/app is 100% [TypeScript](https://www.typescriptlang.org/).

### Utilities

This Turborepo has some additional tools already setup for you:

- [TypeScript](https://www.typescriptlang.org/) for static type checking
- [ESLint](https://eslint.org/) for code linting
- [Prettier](https://prettier.io) for code formatting

### Build

To build all apps and packages, run the following command:

With [global `turbo`](https://turborepo.dev/docs/getting-started/installation#global-installation) installed (recommended):

```sh
cd my-turborepo
turbo build
```

Without global `turbo`, use your package manager:

```sh
cd my-turborepo
npx turbo build
pnpm dlx turbo build
pnpm exec turbo build
```

You can build a specific package by using a [filter](https://turborepo.dev/docs/crafting-your-repository/running-tasks#using-filters):

With [global `turbo`](https://turborepo.dev/docs/getting-started/installation#global-installation) installed:

```sh
turbo build --filter=docs
```

Without global `turbo`:

```sh
npx turbo build --filter=docs
pnpm exec turbo build --filter=docs
pnpm exec turbo build --filter=docs
```

### Develop

To develop all apps and packages, run the following command:

With [global `turbo`](https://turborepo.dev/docs/getting-started/installation#global-installation) installed (recommended):

```sh
cd my-turborepo
turbo dev
```

Without global `turbo`, use your package manager:

```sh
cd my-turborepo
npx turbo dev
pnpm exec turbo dev
pnpm exec turbo dev
```

You can develop a specific package by using a [filter](https://turborepo.dev/docs/crafting-your-repository/running-tasks#using-filters):

With [global `turbo`](https://turborepo.dev/docs/getting-started/installation#global-installation) installed:

```sh
turbo dev --filter=web
```

Without global `turbo`:

```sh
npx turbo dev --filter=web
pnpm exec turbo dev --filter=web
pnpm exec turbo dev --filter=web
```

### Remote Caching

> [!TIP]
> Vercel Remote Cache is free for all plans. Get started today at [vercel.com](https://vercel.com/signup?utm_source=remote-cache-sdk&utm_campaign=free_remote_cache).

Turborepo can use a technique known as [Remote Caching](https://turborepo.dev/docs/core-concepts/remote-caching) to share cache artifacts across machines, enabling you to share build caches with your team and CI/CD pipelines.

By default, Turborepo will cache locally. To enable Remote Caching you will need an account with Vercel. If you don't have an account you can [create one](https://vercel.com/signup?utm_source=turborepo-examples), then enter the following commands:

With [global `turbo`](https://turborepo.dev/docs/getting-started/installation#global-installation) installed (recommended):

```sh
cd my-turborepo
turbo login
```

Without global `turbo`, use your package manager:

```sh
cd my-turborepo
npx turbo login
pnpm exec turbo login
pnpm exec turbo login
```

This will authenticate the Turborepo CLI with your [Vercel account](https://vercel.com/docs/concepts/personal-accounts/overview).

Next, you can link your Turborepo to your Remote Cache by running the following command from the root of your Turborepo:

With [global `turbo`](https://turborepo.dev/docs/getting-started/installation#global-installation) installed:

```sh
turbo link
```

Without global `turbo`:

```sh
npx turbo link
pnpm exec turbo link
pnpm exec turbo link
```

## Useful Links

Learn more about the power of Turborepo:

- [Tasks](https://turborepo.dev/docs/crafting-your-repository/running-tasks)
- [Caching](https://turborepo.dev/docs/crafting-your-repository/caching)
- [Remote Caching](https://turborepo.dev/docs/core-concepts/remote-caching)
- [Filtering](https://turborepo.dev/docs/crafting-your-repository/running-tasks#using-filters)
- [Configuration Options](https://turborepo.dev/docs/reference/configuration)
- [CLI Usage](https://turborepo.dev/docs/reference/command-line-reference)

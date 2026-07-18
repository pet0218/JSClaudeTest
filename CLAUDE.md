# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project context

This is the starter project for a Claude Code course (codewithmosh.com). It's a small React + Vite expense tracker that **intentionally** ships with a bug, poor UI, and messy code, meant to be fixed incrementally. Don't assume rough edges are accidental — some are the deliberate starting point for exercises.

## Commands

```bash
npm install      # install dependencies
npm run dev      # start Vite dev server at http://localhost:5173
npm run build    # production build
npm run preview  # preview the production build locally
npm run lint     # run ESLint over the project
```

There is no test runner configured in this project.

## Architecture

This is a minimal, single-component Vite + React app — there is no router, state management library, or backend.

- `src/main.jsx` — entry point, mounts `App` into `#root`.
- `src/App.jsx` — the entire application: transaction state, the add-transaction form, filters, and the summary/table UI all live in one component with local `useState` hooks. There is no separate data layer, API, or persistence (state resets on reload).
- `src/App.css` / `src/index.css` — styling.

Notable existing behavior worth knowing before "fixing" it unprompted: transaction `amount` values are stored as strings (from form input and seed data), and the income/expense totals are computed with `reduce((sum, t) => sum + t.amount, 0)` — without numeric coercion this concatenates rather than sums.

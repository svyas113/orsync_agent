# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

## Or-sync chat widget

`src/components/ChatWidget.jsx` embeds the visitor agent on every page.

1. Copy `.env.example` → `.env` and set `VITE_AGENT_API_URL` to the FastAPI agent origin.
2. Run the agent with `../run_orsync_visitor.sh` (default `http://localhost:8003`).
3. `npm run dev` — open the site and use the floating **Chat** button.

See `../README.md` for training, SMTP (Gmail app password), and demo URL configuration.

import js from "@eslint/js";
import globals from "globals";

// Revisa el JavaScript de la página (web/). Las Lambdas son Python y no pasan por aquí.
export default [
  { ignores: ["node_modules/"] },
  js.configs.recommended,
  {
    files: ["web/**/*.js"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "script",
      globals: { ...globals.browser },
    },
    rules: {
      // Reglas pensadas para evitar ejecución de código inyectado.
      "no-eval": "error",
      "no-implied-eval": "error",
      "no-new-func": "error",
      "no-script-url": "error",
      // Calidad general.
      eqeqeq: "error",
      "no-var": "error",
      "prefer-const": "error",
    },
  },
];

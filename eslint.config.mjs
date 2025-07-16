// Импорт встроенной конфигурации ESLint для JavaScript
import js from "@eslint/js";
import globals from "globals"; // Импорт набора глобальных переменных браузера и Node.js
import pluginReact from "eslint-plugin-react";
import { defineConfig } from "eslint/config";

// Главный экспорт конфигурации
export default defineConfig([
  { files: ["**/*.{js,mjs,cjs,jsx}"], plugins: { js }, extends: ["js/recommended"] },
  { files: ["**/*.js"], languageOptions: { sourceType: "commonjs" } }, //указываем, что используется CommonJS (require/module.exports)
  { files: ["**/*.{js,mjs,cjs,jsx}"], languageOptions: { globals: globals.browser } },  // 3. Указываем глобальные переменные, допустимые в браузере (window, alert и т.д.)
  pluginReact.configs.flat.recommended,
]);
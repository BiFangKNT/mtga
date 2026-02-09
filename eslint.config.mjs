import withNuxt from "./.nuxt/eslint.config.mjs"
import betterTailwind from "eslint-plugin-better-tailwindcss"
import * as yamlParser from "yaml-eslint-parser"
import * as eslintPluginYml from "eslint-plugin-yml"

export default withNuxt(
  {
    ignores: [
      "node_modules",
      ".nuxt",
      ".output",
      "dist",
      "archive",
      "src-tauri",
      "python-src",
      "pnpm-lock.yaml",
    ],
  },
  {
    files: ["**/*.{ts,tsx,vue}"],
    languageOptions: {
      parserOptions: {
        projectService: true,
        tsconfigRootDir: process.cwd(),
      },
    },
    rules: {
      "@typescript-eslint/no-unsafe-type-assertion": "warn",
      "@typescript-eslint/no-unnecessary-type-assertion": "warn",
    },
  },
  // 添加 YAML 支持
  {
    files: ["**/*.{yaml,yml}"],
    languageOptions: {
      parser: yamlParser,
    },
    plugins: {
      yml: eslintPluginYml.default || eslintPluginYml,
    },
    rules: {
      // 对应 document-start: present: false
      "yml/file-header": "off",

      // 对应 indentation: spaces: 2, indent-sequences: true
      "yml/indent": ["error", 2, { indentBlockSequences: true }],

      // YAML 插件本身没有 line-length，使用 ESLint 通用规则或关闭
      "max-len": ["warn", { code: 175, ignoreUrls: true }],

      // 对应 trailing-spaces: level: warning
      "no-trailing-spaces": "warn",

      // 对应 comments: min-spaces-from-content: 1
      "yml/spaced-comment": ["error", "always"],
    },
  },
  // 添加 Better Tailwind CSS 支持
  {
    plugins: {
      "better-tailwindcss": betterTailwind,
    },
    rules: {
      // 使用 warn 级别而不是 error，避免阻塞开发
      ...Object.fromEntries(
        Object.entries(betterTailwind.configs.recommended.rules).map(([key, value]) => [
          key,
          value === "error" ? "warn" : value,
        ])
      ),
      "better-tailwindcss/no-unregistered-classes": "off", // daisyUI 类名经常被识别为未注册，暂时关闭
      "better-tailwindcss/enforce-consistent-class-order": "off", // 排序规则太严格，暂时关闭
      "better-tailwindcss/enforce-consistent-line-wrapping": "off", // 换行规则太严格，暂时关闭
      "vue/multi-word-component-names": "off", // 允许单单词组件名
      "vue/html-self-closing": "off", // 允许在 HTML void elements 上使用自闭合
      "@typescript-eslint/unified-signatures": "off", // 允许分开定义重载（在 defineEmits 中常见）
    },
    settings: {
      "better-tailwindcss": {
        // Tailwind v4 的 CSS 入口文件
        entryPoint: "app/assets/css/tailwind.css",
      },
    },
  }
)

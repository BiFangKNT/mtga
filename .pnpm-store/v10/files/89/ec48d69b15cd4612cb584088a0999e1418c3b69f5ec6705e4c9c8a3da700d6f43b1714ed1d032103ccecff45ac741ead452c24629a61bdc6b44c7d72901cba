import { Linter } from 'eslint';

interface Options {
    blocks?: {
        /**
         * Create virtual files for each `<style>` block
         * @default false
         */
        styles?: boolean;
        /**
         * Enable custom blocks
         * Pass an string array to specify custom block types, or `true` to enable all custom blocks
         * @default false
         */
        customBlocks?: boolean | string[];
        /**
         * Create virtual files for each `<template>` block
         * Generally not recommended, as `eslint-plugin-vue` handles it
         * @default false
         */
        template?: boolean;
        /**
         * Create virtual files for each `<script>` block
         * Generally not recommended, as `eslint-plugin-vue` handles it
         * @default false
         */
        script?: boolean;
        /**
         * Create virtual files for each `<script setup>` block
         * Generally not recommended, as `eslint-plugin-vue` handles it
         * @default false
         */
        scriptSetup?: boolean;
    };
    /**
     * Default language for each block type
     *
     * @example { style: 'postcss', i18n: 'json' }
     */
    defaultLanguage?: Record<string, string>;
}
declare function processor(options?: Options): Linter.Processor;

export { type Options, processor as default };

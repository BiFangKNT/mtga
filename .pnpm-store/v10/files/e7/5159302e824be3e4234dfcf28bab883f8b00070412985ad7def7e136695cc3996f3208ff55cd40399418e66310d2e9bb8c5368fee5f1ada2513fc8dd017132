<script setup>
import { computed, getCurrentInstance, onBeforeUnmount, ref } from "vue";
import { onPrehydrate } from "../composables/ssr";
import { useNuxtApp } from "../nuxt";
const props = defineProps({
  locale: { type: String, required: false },
  datetime: { type: [String, Number, Date], required: true },
  localeMatcher: { type: String, required: false },
  weekday: { type: String, required: false },
  era: { type: String, required: false },
  year: { type: String, required: false },
  month: { type: String, required: false },
  day: { type: String, required: false },
  hour: { type: String, required: false },
  minute: { type: String, required: false },
  second: { type: String, required: false },
  timeZoneName: { type: String, required: false },
  formatMatcher: { type: String, required: false },
  hour12: { type: Boolean, required: false, default: void 0 },
  timeZone: { type: String, required: false },
  calendar: { type: String, required: false },
  dayPeriod: { type: String, required: false },
  numberingSystem: { type: String, required: false },
  dateStyle: { type: String, required: false },
  timeStyle: { type: String, required: false },
  hourCycle: { type: String, required: false },
  relative: { type: Boolean, required: false },
  numeric: { type: String, required: false },
  relativeStyle: { type: String, required: false },
  title: { type: [Boolean, String], required: false }
});
const el = getCurrentInstance()?.vnode.el;
const renderedDate = el?.getAttribute("datetime");
const _locale = el?.getAttribute("data-locale");
const nuxtApp = useNuxtApp();
const date = computed(() => {
  const date2 = props.datetime;
  if (renderedDate && nuxtApp.isHydrating) {
    return new Date(renderedDate);
  }
  if (!props.datetime) {
    return /* @__PURE__ */ new Date();
  }
  return new Date(date2);
});
const now = ref(import.meta.client && nuxtApp.isHydrating && window._nuxtTimeNow ? new Date(window._nuxtTimeNow) : /* @__PURE__ */ new Date());
if (import.meta.client && props.relative) {
  const handler = () => {
    now.value = /* @__PURE__ */ new Date();
  };
  const interval = setInterval(handler, 1e3);
  onBeforeUnmount(() => clearInterval(interval));
}
const formatter = computed(() => {
  const { locale: propsLocale, relative, relativeStyle, ...rest } = props;
  if (relative) {
    return new Intl.RelativeTimeFormat(_locale ?? propsLocale, { ...rest, style: relativeStyle });
  }
  return new Intl.DateTimeFormat(_locale ?? propsLocale, rest);
});
const formattedDate = computed(() => {
  if (isInvalidDate.value) {
    return date.value.toString();
  }
  if (!props.relative) {
    return formatter.value.format(date.value);
  }
  const diffInSeconds = (date.value.getTime() - now.value.getTime()) / 1e3;
  const units = [
    { unit: "second", seconds: 1, threshold: 60 },
    // 60 seconds → minute
    { unit: "minute", seconds: 60, threshold: 60 },
    // 60 minutes → hour
    { unit: "hour", seconds: 3600, threshold: 24 },
    // 24 hours → day
    { unit: "day", seconds: 86400, threshold: 30 },
    // ~30 days → month
    { unit: "month", seconds: 2592e3, threshold: 12 },
    // 12 months → year
    { unit: "year", seconds: 31536e3, threshold: Infinity }
  ];
  const { unit, seconds } = units.find(({ seconds: seconds2, threshold }) => Math.abs(diffInSeconds / seconds2) < threshold) || units[units.length - 1];
  const value = diffInSeconds / seconds;
  return formatter.value.format(Math.round(value), unit);
});
const isInvalidDate = computed(() => Number.isNaN(date.value.getTime()));
const isoDate = computed(() => isInvalidDate.value ? void 0 : date.value.toISOString());
const title = computed(() => props.title === true ? isoDate.value : typeof props.title === "string" ? props.title : void 0);
const dataset = {};
if (import.meta.server) {
  for (const prop in props) {
    if (prop !== "datetime") {
      const value = props?.[prop];
      if (value) {
        const propInKebabCase = prop.split(/(?=[A-Z])/).join("-");
        dataset[`data-${propInKebabCase}`] = props?.[prop];
      }
    }
  }
  onPrehydrate((el2) => {
    const now2 = window._nuxtTimeNow ||= Date.now();
    const toCamelCase = (name, index) => {
      if (index > 0) {
        return name[0].toUpperCase() + name.slice(1);
      }
      return name;
    };
    const datetime = el2.getAttribute("datetime");
    if (!datetime) {
      return;
    }
    const date2 = new Date(datetime);
    if (Number.isNaN(date2.getTime())) {
      return;
    }
    const options = {};
    for (const name of el2.getAttributeNames()) {
      if (name.startsWith("data-")) {
        let optionName = name.slice(5).split("-").map(toCamelCase).join("");
        if (optionName === "relativeStyle") {
          optionName = "style";
        }
        options[optionName] = el2.getAttribute(name);
      }
    }
    if (options.relative) {
      const diffInSeconds = (date2.getTime() - now2) / 1e3;
      const units = [
        { unit: "second", seconds: 1, threshold: 60 },
        // 60 seconds → minute
        { unit: "minute", seconds: 60, threshold: 60 },
        // 60 minutes → hour
        { unit: "hour", seconds: 3600, threshold: 24 },
        // 24 hours → day
        { unit: "day", seconds: 86400, threshold: 30 },
        // ~30 days → month
        { unit: "month", seconds: 2592e3, threshold: 12 },
        // 12 months → year
        { unit: "year", seconds: 31536e3, threshold: Infinity }
      ];
      const { unit, seconds } = units.find(({ seconds: seconds2, threshold }) => Math.abs(diffInSeconds / seconds2) < threshold) || units[units.length - 1];
      const value = diffInSeconds / seconds;
      const formatter2 = new Intl.RelativeTimeFormat(options.locale, options);
      el2.textContent = formatter2.format(Math.round(value), unit);
    } else {
      const formatter2 = new Intl.DateTimeFormat(options.locale, options);
      el2.textContent = formatter2.format(date2);
    }
  });
}
</script>

<template>
  <time
    v-bind="dataset"
    :datetime="isoDate"
    :title="title"
  >{{ formattedDate }}</time>
</template>

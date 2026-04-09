import { buildHtml } from "./html.js";
import { outputPlainTextList } from "./list.js";
import { outputMarkdown } from "./markdown.js";
import { outputRawData } from "./raw-data.js";
const TEMPLATE_TYPE_RENDERED = {
    network: buildHtml("network"),
    sunburst: buildHtml("sunburst"),
    treemap: buildHtml("treemap"),
    "treemap-3d": buildHtml("treemap-3d"),
    "raw-data": async ({ data }) => outputRawData(data),
    list: async ({ data }) => outputPlainTextList(data),
    markdown: async ({ data, reportConfig }) => outputMarkdown(data, reportConfig),
    flamegraph: buildHtml("flamegraph"),
};
export const renderTemplate = (templateType, options) => {
    return TEMPLATE_TYPE_RENDERED[templateType](options);
};

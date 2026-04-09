import { VueElementConstructor } from 'vue';
import { ElementTraceInfo } from 'vite-plugin-vue-tracer/client/record';

declare const NuxtDevtoolsFrame: VueElementConstructor;

interface NuxtDevToolsInspectorProps {
    matched?: ElementTraceInfo;
    hasParent?: boolean;
    mouse: {
        x: number;
        y: number;
    };
}

declare const NuxtDevtoolsInspectPanel: VueElementConstructor<{
    props: NuxtDevToolsInspectorProps;
}>;

export { NuxtDevtoolsFrame, NuxtDevtoolsInspectPanel };
export type { NuxtDevToolsInspectorProps };

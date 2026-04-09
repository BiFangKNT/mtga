import * as vue from 'vue';
import { ElementTraceInfo } from './record.mjs';
export { PositionInfo, findTraceAtPointer, findTraceFromElement, findTraceFromVNode, getInternalStore, hasData, recordPosition } from './record.mjs';
export { Events, events, isEnabled, lastMatchedElement } from './listeners.mjs';

declare const state: {
    isEnabled: boolean;
    isVisible: boolean;
    isAnimated: boolean;
    isFocused: boolean;
    main?: {
        pos: [source: string, line: number, column: number];
        vnode: vue.VNode | undefined;
        el: Element | undefined;
        readonly filepath: string;
        readonly fullpath: string;
        readonly rect: {
            height: number;
            width: number;
            x: number;
            y: number;
            readonly bottom: number;
            readonly left: number;
            readonly right: number;
            readonly top: number;
            toJSON: () => any;
        } | undefined;
        getElementsSameFile: () => Element[] | undefined;
        getParent: () => ElementTraceInfo | undefined;
        getElementsSamePosition: () => Element[] | undefined;
    } | undefined;
    sub: {
        rects?: {
            id: string;
            rect: {
                height: number;
                width: number;
                x: number;
                y: number;
                readonly bottom: number;
                readonly left: number;
                readonly right: number;
                readonly top: number;
                toJSON: () => any;
            };
        }[] | undefined;
    };
};

export { ElementTraceInfo, state };

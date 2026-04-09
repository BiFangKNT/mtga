import './shared/devtools.C1a10l_c.mjs';
import { ModuleStaticInfo } from '@nuxt/devtools-kit/types';
export * from '@nuxt/devtools-kit/types';

interface SocialPreviewResolved {
    url?: string;
    title?: string;
    description?: string;
    favicon?: string;
    image?: string;
    imageAlt?: string;
}
interface SocialPreviewCard {
    url?: SocialPreviewCardItem[];
    title?: SocialPreviewCardItem[];
    description?: SocialPreviewCardItem[];
    favicon?: SocialPreviewCardItem[];
    image?: SocialPreviewCardItem[];
    imageAlt?: SocialPreviewCardItem[];
}
interface SocialPreviewCardItem {
    tag: string;
    name?: string;
}
interface NormalizedHeadTag {
    tag: string;
    name: string;
    value: string;
}
interface InstallingModulestate {
    name: string;
    info: ModuleStaticInfo;
    processId: string;
}
interface AnalyzeBuildingState {
    name: string;
    processId: string;
}
type ModuleActionType = 'install' | 'uninstall';

export type { AnalyzeBuildingState, InstallingModulestate, ModuleActionType, NormalizedHeadTag, SocialPreviewCard, SocialPreviewResolved };

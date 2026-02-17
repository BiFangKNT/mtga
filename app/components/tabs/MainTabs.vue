<script setup lang="ts">
import type { MainTabKey } from "~/composables/mtgaTypes"

const tabs: { key: MainTabKey; label: string }[] = [
  { key: "cert", label: "证书管理" },
  { key: "hosts", label: "hosts接管" },
  { key: "proxy", label: "代理服务" },
];

const activeTab = ref<MainTabKey>("cert");
const direction = ref<"right" | "left">("right");
const { mainTabTarget, mainTabSignal } = useMtgaStore()

/**
 * 处理标签页切换
 * @param key 目标标签页的键名
 */
const selectTab = (key: MainTabKey) => {
  const oldIndex = tabs.findIndex((t) => t.key === activeTab.value);
  const newIndex = tabs.findIndex((t) => t.key === key);

  if (newIndex !== oldIndex) {
    direction.value = newIndex > oldIndex ? "right" : "left";
    activeTab.value = key;
  }
};

const applyMainTabTarget = (target: MainTabKey | null) => {
  if (!target) {
    return
  }
  selectTab(target)
}

watch(mainTabSignal, () => applyMainTabTarget(mainTabTarget.value), {
  immediate: true,
})
</script>

<template>
  <div class="flex flex-wrap items-center justify-between gap-3">
    <div>
      <h2 class="mtga-card-title">核心服务</h2>
      <p class="mtga-card-subtitle">证书管理 / hosts接管 / 代理服务</p>
    </div>
    <span class="mtga-chip">核心服务</span>
  </div>
  <div role="tablist" class="mt-4 flex flex-wrap gap-3 border-b border-slate-200/70 pb-2">
    <button
      v-for="tab in tabs"
      :key="tab.key"
      role="tab"
      type="button"
      class="cursor-pointer px-3 py-2 text-sm font-medium text-slate-500 transition-colors duration-150"
      :class="activeTab === tab.key ? 'border-b-2 border-amber-500 text-slate-900' : 'border-b-2 border-transparent hover:text-slate-800'"
      :aria-selected="activeTab === tab.key"
      @click="selectTab(tab.key)"
    >
      {{ tab.label }}
    </button>
  </div>

  <Transition
    enter-active-class="transition duration-200 ease-out"
    :enter-from-class="direction === 'right' ? 'opacity-0 translate-x-8' : 'opacity-0 -translate-x-8'"
    enter-to-class="opacity-100 translate-x-0"
    leave-active-class="transition duration-150 ease-in"
    leave-from-class="opacity-100 translate-x-0"
    :leave-to-class="direction === 'right' ? 'opacity-0 -translate-x-8' : 'opacity-0 translate-x-8'"
    mode="out-in"
  >
    <div :key="activeTab" class="mt-4 space-y-4">
      <section v-if="activeTab === 'cert'">
        <CertTab />
      </section>
      <section v-else-if="activeTab === 'hosts'">
        <HostsTab />
      </section>
      <section v-else-if="activeTab === 'proxy'">
        <ProxyTab />
      </section>
    </div>
  </Transition>
</template>

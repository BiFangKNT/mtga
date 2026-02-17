<template>
  <div class="h-full flex flex-col bg-base-200/50 backdrop-blur-sm rounded-box border border-base-content/5">
    <div ref="logContainer" class="flex-1 overflow-y-auto p-4 space-y-1 font-mono text-xs">
      <div v-for="(log, index) in logs" :key="index" class="break-all whitespace-pre-wrap text-base-content/80 hover:text-base-content transition-colors">
        {{ log }}
      </div>
      <div v-if="logs.length === 0" class="h-full flex items-center justify-center text-base-content/30 italic">
        暂无日志
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'

const props = defineProps<{
  logs: string[]
}>()

const logContainer = ref<HTMLElement | null>(null)

watch(() => props.logs, () => {
  nextTick(() => {
    if (logContainer.value) {
      logContainer.value.scrollTop = logContainer.value.scrollHeight
    }
  })
}, { deep: true })
</script>

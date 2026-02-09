<script setup lang="ts">
const store = useMtgaStore()
const options = store.runtimeOptions
const outboundProxyTypes = store.outboundProxyTypes
const proxyEnabled = computed({
  get: () => store.outboundProxyEnabled.value,
  set: (value) => {
    store.outboundProxyEnabled.value = value
  },
})
const proxyType = computed({
  get: () => store.outboundProxyType.value,
  set: (value) => {
    store.outboundProxyType.value = value
  },
})
const proxyHost = computed({
  get: () => store.outboundProxyHost.value,
  set: (value) => {
    store.outboundProxyHost.value = value
  },
})
const proxyPort = computed({
  get: () => store.outboundProxyPort.value,
  set: (value) => {
    store.outboundProxyPort.value = value
  },
})
const proxyUsername = computed({
  get: () => store.outboundProxyUsername.value,
  set: (value) => {
    store.outboundProxyUsername.value = value
  },
})
const proxyPassword = computed({
  get: () => store.outboundProxyPassword.value,
  set: (value) => {
    store.outboundProxyPassword.value = value
  },
})
const saving = ref(false)

const debugModeTooltip = [
  "开启后：",
  "1) 代理服务器输出更详细的调试日志，便于排查问题；",
  "2) 启动代理服务器前会额外检查系统/环境变量的显式代理配置",
  "并提示其可能绕过 hosts 导流。",
  "（默认不做第 2 项检查，仅在调试模式下启用）",
].join("\n")

const handleStart = () => {
  store.runProxyStart()
}

const handleStop = () => {
  store.runProxyStop()
}

const handleCheck = () => {
  store.runProxyCheckNetwork()
}

const proxyHostError = computed(() => {
  if (!proxyEnabled.value) {
    return ""
  }
  if (!proxyHost.value.trim()) {
    return "代理地址必填"
  }
  return ""
})

const proxyPortError = computed(() => {
  if (!proxyEnabled.value) {
    return ""
  }
  const text = proxyPort.value.trim()
  if (!text) {
    return "代理端口必填"
  }
  const port = Number.parseInt(text, 10)
  if (!Number.isFinite(port) || port <= 0 || port > 65535) {
    return "代理端口需为 1-65535"
  }
  return ""
})

const handleSaveProxy = async () => {
  if (proxyHostError.value || proxyPortError.value) {
    store.appendLog("错误: 代理地址和端口为必填项")
    return
  }
  saving.value = true
  const ok = await store.saveConfig()
  saving.value = false
  if (ok) {
    store.appendLog("网络代理配置已保存")
  } else {
    store.appendLog("保存网络代理配置失败")
  }
}
</script>

<template>
  <div class="mtga-soft-panel space-y-4 mb-4">
    <div>
      <div class="text-sm font-semibold text-slate-900">网络代理</div>
      <div class="text-xs text-slate-500">配置出站网络访问代理</div>
    </div>
    <label class="flex items-center gap-3 text-sm text-slate-700 cursor-pointer hover:bg-slate-100/50 rounded px-3 py-2 -my-1 transition-colors">
      <input v-model="proxyEnabled" type="checkbox" class="checkbox checkbox-sm" />
      <span>启用网络代理</span>
    </label>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
      <MtgaSelect
        v-model="proxyType"
        :options="outboundProxyTypes"
        label="代理类型"
        :disabled="!proxyEnabled"
      />
      <MtgaInput
        v-model="proxyHost"
        label="代理地址"
        placeholder="例如：127.0.0.1"
        :disabled="!proxyEnabled"
        :error="proxyHostError"
      />
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
      <MtgaInput
        v-model="proxyPort"
        label="代理端口"
        type="number"
        placeholder="例如：7890"
        :disabled="!proxyEnabled"
        :error="proxyPortError"
      />
      <MtgaInput
        v-model="proxyUsername"
        label="用户名"
        placeholder="可选"
        :disabled="!proxyEnabled"
      />
      <MtgaInput
        v-model="proxyPassword"
        label="密码"
        type="password"
        placeholder="可选"
        :disabled="!proxyEnabled"
      />
    </div>
    <div class="flex items-center justify-between gap-3">
      <span class="text-xs text-slate-500">保存后会写入现有配置文件</span>
      <button
        class="btn btn-primary btn-sm px-4 rounded-xl"
        :disabled="saving"
        @click="handleSaveProxy"
      >
        保存网络代理配置
      </button>
    </div>
  </div>

  <div class="mtga-soft-panel space-y-3 mb-4">
    <div>
      <div class="text-sm font-semibold text-slate-900">运行时选项</div>
      <div class="text-xs text-slate-500">控制代理运行行为与调试细节</div>
    </div>
    <div class="space-y-3">
      <label
        class="flex items-center gap-3 text-sm text-slate-700 tooltip mtga-tooltip cursor-pointer hover:bg-slate-100/50 rounded px-3 py-2 -my-1 transition-colors"
        :data-tip="debugModeTooltip"
        style="--mtga-tooltip-max: 500px;"
      >
        <input v-model="options.debugMode" type="checkbox" class="checkbox checkbox-sm" />
        <span>开启调试模式</span>
      </label>
      <label class="flex items-center gap-3 text-sm text-slate-700 cursor-pointer hover:bg-slate-100/50 rounded px-3 py-2 -my-1 transition-colors">
        <input
          v-model="options.disableSslStrict"
          type="checkbox"
          class="checkbox checkbox-sm"
        />
        <span>关闭SSL严格模式</span>
      </label>
      <div class="flex flex-wrap items-center gap-1 text-sm text-slate-700">
        <label class="flex items-center gap-3 cursor-pointer hover:bg-slate-100/50 rounded px-3 py-2 -my-1 transition-colors">
          <input
            v-model="options.forceStream"
            type="checkbox"
            class="checkbox checkbox-sm"
          />
          <span>强制流模式</span>
        </label>
        <MtgaSelect
          v-model="options.streamMode"
          :options="['true', 'false']"
          size="xs"
          class="w-20"
          :disabled="!options.forceStream"
        />
      </div>
    </div>
  </div>

  <div class="mtga-soft-panel space-y-3">
    <div>
      <div class="text-sm font-semibold text-slate-900">代理服务</div>
      <div class="text-xs text-slate-500">启动 / 停止 / 网络检查</div>
    </div>
    <div class="space-y-2">
      <button class="mtga-btn-primary" @click="handleStart">启动代理服务器</button>
      <button class="mtga-btn-error" @click="handleStop">停止代理服务器</button>
      <button class="mtga-btn-outline" @click="handleCheck">检查网络环境</button>
    </div>
  </div>
</template>

<script setup lang="ts">
const store = useMtgaStore()
const saving = ref(false)
const mappedModelId = computed({
  get: () => store.mappedModelId.value,
  set: (value) => {
    store.mappedModelId.value = value
  },
})
const mtgaAuthKey = computed({
  get: () => store.mtgaAuthKey.value,
  set: (value) => {
    store.mtgaAuthKey.value = value
  },
})

const mappedModelTooltip = [
  "必填：全局映射模型ID",
  "这是您在 Trae/Cursor 等客户端中填写的【模型名称】。",
  "MTGA 会截获此模型名称的请求，并转发到配置分组中定义的【实际模型ID】。",
  "示例：gpt-5",
].join("\n")

const mtgaAuthTooltip = [
  "必填：MTGA 全局鉴权密钥",
  "这是您在 Trae/Cursor 等客户端中填写的【API Key】。",
  "客户端必须使用此 Key 才能连接到 MTGA 代理服务。",
  "这与配置分组中的上游 API Key 是相互独立的。",
  "示例：111",
].join("\n")

const handleSave = async () => {
  if (!store.mappedModelId.value || !store.mtgaAuthKey.value) {
    store.appendLog("错误: 映射模型ID和MTGA鉴权Key都是必填项")
    return
  }
  saving.value = true
  const ok = await store.saveConfig()
  saving.value = false
  if (ok) {
    store.appendLog("全局配置已保存")
  } else {
    store.appendLog("保存全局配置失败")
  }
}
</script>

<template>
  <div class="flex items-center justify-between gap-3">
    <div>
      <h2 class="mtga-card-title">全局参数</h2>
      <p class="mtga-card-subtitle">定义客户端（如 Trae/Cursor）连接 MTGA 的认证信息与模型映射</p>
    </div>
    <span class="mtga-chip">全局参数</span>
  </div>
  <div class="mt-4 space-y-4">
    <div class="mtga-soft-panel space-y-4">
      <div
        class="tooltip mtga-tooltip w-full"
        :data-tip="mappedModelTooltip"
        style="--mtga-tooltip-max: 360px;"
      >
        <MtgaInput 
          v-model="mappedModelId"
          label="映射模型ID"
          placeholder="例如：gpt-5"
          required
        />
      </div>

      <div
        class="tooltip mtga-tooltip w-full"
        :data-tip="mtgaAuthTooltip"
        style="--mtga-tooltip-max: 360px;"
      >
        <MtgaInput 
          v-model="mtgaAuthKey"
          label="MTGA鉴权Key"
          placeholder="例如：111"
          type="password"
          required
        />
      </div>
    </div>

    <div class="flex items-center justify-between gap-3">
      <span class="text-xs text-slate-500">保存后会同步所有配置组</span>
      <button
        class="btn btn-primary btn-sm px-4 rounded-xl"
        :disabled="saving"
        @click="handleSave"
      >
        保存全局配置
      </button>
    </div>
  </div>
</template>

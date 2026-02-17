// 开机自启动功能封装
import { ref } from 'vue'

// 检查是否支持自启动功能
export async function isAutoStartSupported(): Promise<boolean> {
    if (!import.meta.client || typeof window === 'undefined') {
        return false
    }

    try {
        // 尝试加载Tauri autostart插件
        // 注意：在开发环境(pnpm dev)下，window.__TAURI__ 可能存在，但 autostart 插件可能无法工作
        // 因为它需要注册表权限或特定的安装路径
        const { isEnabled } = await import('@tauri-apps/plugin-autostart')
        // 简单调用一次检查，如果报错说明不支持或未配置
        await isEnabled()
        return true
    } catch (error) {
        console.warn('[AutoStart] Plugin check failed (dev environment?):', error)
        return false
    }
}

// 检查自启动是否已启用
export async function isAutoStartEnabled(): Promise<boolean> {
    try {
        const { isEnabled } = await import('@tauri-apps/plugin-autostart')
        const enabled = await isEnabled()
        console.log('[AutoStart] Current status:', enabled)
        return enabled
    } catch (error) {
        console.error('[AutoStart] Failed to get status:', error)
        return false
    }
}

// 启用开机自启动
export async function enableAutoStart(): Promise<boolean> {
    try {
        const { enable } = await import('@tauri-apps/plugin-autostart')
        console.log('[AutoStart] Attempting to ENABLE...')
        await enable()
        console.log('[AutoStart] ENABLE command sent.')

        // 双重检查
        const confirmed = await isAutoStartEnabled()
        if (confirmed) {
            console.log('[AutoStart] Successfully ENABLED.')
            return true
        } else {
            console.warn('[AutoStart] ENABLE command sent but status is still FALSE. (Dev environment limitation?)')
            return false
        }
    } catch (error) {
        console.error('[AutoStart] Failed to enable:', error)
        throw error
    }
}

// 禁用开机自启动
export async function disableAutoStart(): Promise<boolean> {
    try {
        const { disable } = await import('@tauri-apps/plugin-autostart')
        console.log('[AutoStart] Attempting to DISABLE...')
        await disable()
        console.log('[AutoStart] DISABLE command sent.')

        const confirmed = await isAutoStartEnabled()
        if (!confirmed) {
            console.log('[AutoStart] Successfully DISABLED.')
            return true
        } else {
            console.warn('[AutoStart] DISABLE command sent but status is still TRUE.')
            return false
        }
    } catch (error) {
        console.error('[AutoStart] Failed to disable:', error)
        throw error
    }
}

// 切换开机自启动状态
export async function toggleAutoStart(enabled: boolean): Promise<boolean> {
    if (enabled) {
        return await enableAutoStart()
    } else {
        return await disableAutoStart()
    }
}

// 获取当前自启动状态
export function useAutoStart() {
    const isSupported = ref(false)
    const isEnabled = ref(false)
    const isLoading = ref(false)

    // 初始化时检查自启动状态
    // 注意：onMounted 只能在组件的 setup() 或 <script setup> 中使用
    // 如果在普通 JS/TS 文件或异步函数中调用会报错
    // 这里我们不再自动调用，而是让组件手动调用 checkStatus()

    const checkStatus = async () => {
        if (isLoading.value || !import.meta.client) return

        isLoading.value = true
        try {
            const supported = await isAutoStartSupported()
            isSupported.value = supported

            if (supported) {
                const enabled = await isAutoStartEnabled()
                isEnabled.value = enabled
            } else {
                console.log('[AutoStart] Not supported in current environment')
            }
        } catch (error) {
            console.error('[AutoStart] Status check error:', error instanceof Error ? error.message : String(error))
        } finally {
            isLoading.value = false
        }
    }

    const setEnabled = async (value: boolean) => {
        if (isLoading.value) return

        isLoading.value = true
        try {
            if (value) {
                await enableAutoStart()
            } else {
                await disableAutoStart()
            }
            // 重新检查状态以确认
            const current = await isAutoStartEnabled()
            isEnabled.value = current

            // 如果状态没有改变，抛出错误以便UI提示
            if (current !== value) {
                throw new Error(
                    '操作看似成功但状态未改变。' +
                    (import.meta.dev ? ' (开发环境下自启动功能通常不可用，请打包后测试)' : '')
                )
            }
        } catch (error) {
            console.error('[AutoStart] Toggle error:', error)
            throw error
        } finally {
            isLoading.value = false
        }
    }

    return {
        isSupported,
        isEnabled,
        isLoading,
        checkStatus,
        setEnabled
    }
}

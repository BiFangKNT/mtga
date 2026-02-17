// 系统托盘功能封装
import { ref } from 'vue'
import { TrayIcon } from '@tauri-apps/api/tray'
import { Menu } from '@tauri-apps/api/menu'
import { getCurrentWindow } from '@tauri-apps/api/window'
import { invoke } from '@tauri-apps/api/core'
import type { TrayIconEvent } from '@tauri-apps/api/tray'
import { resolveResource } from '@tauri-apps/api/path'
import { Image } from '@tauri-apps/api/image'

import { defaultWindowIcon } from '@tauri-apps/api/app'

export function useTray() {
  const isInTray = ref(false)
  const trayIcon = ref<TrayIcon | null>(null)
  const trayMenu = ref<Menu | null>(null)

  // 创建系统托盘
  const createTray = async () => {
    // 避免重复创建
    if (trayIcon.value) return

    try {
      console.log('[Tray] Creating system tray...')

      // 创建托盘菜单
      const menu = await Menu.new({
        items: [
          {
            id: 'show',
            text: '显示窗口',
            action: () => {
              showWindow()
            }
          },
          {
            item: 'Separator'
          },
          {
            id: 'quit',
            text: '退出',
            action: () => {
              quitApp()
            }
          }
        ]
      })

      trayMenu.value = menu

      // 获取应用图标作为托盘图标
      let appIcon = null

      // 优先尝试加载 tray-icon.png (从资源目录)
      try {
        const resourcePath = await resolveResource('tray-icon.png')
        appIcon = await Image.fromPath(resourcePath)
        console.log('[Tray] Loaded custom tray icon from resources')
      } catch (e) {
        console.warn('[Tray] Failed to load custom tray icon:', e)
      }

      // 如果自定义图标加载失败，尝试使用默认窗口图标
      if (!appIcon) {
        // 尝试多次获取图标，解决启动时可能的竞争条件
        for (let i = 0; i < 5; i++) {
          try {
            appIcon = await defaultWindowIcon()
            if (appIcon) break
          } catch (e) {
            console.warn(`[Tray] Failed to get default window icon (attempt ${i + 1}):`, e)
          }
          await new Promise(resolve => setTimeout(resolve, 500))
        }
      }

      if (!appIcon) {
        console.warn('[Tray] defaultWindowIcon returned null after retries. System tray might show default OS icon.')
        // 不再使用红色方块 fallback，避免显示丑陋的方块
      }

      // 创建托盘图标
      const icon = await TrayIcon.new({
        tooltip: 'Trae AI',
        icon: appIcon || undefined,
        menu,
        menuOnLeftClick: false, // 默认右键菜单，左键触发 action
        action: (event: TrayIconEvent) => {
          // 处理托盘图标点击事件
          if (event.type === 'Click' && event.button === 'Left') {
            toggleWindow()
          }
        }
      })

      trayIcon.value = icon
      console.log('[Tray] System tray created successfully')

      // 监听窗口事件
      const appWindow = getCurrentWindow()

      // 监听窗口关闭事件
      await appWindow.onCloseRequested(async (event) => {
        event.preventDefault() // 阻止默认关闭行为
        console.log('[Tray] Window close requested, preventing close and hiding to tray')
        await hideToTray()
      })

    } catch (error) {
      console.error('[Tray] Failed to create system tray:', error)
    }
  }

  // 显示窗口
  const showWindow = async () => {
    try {
      const appWindow = getCurrentWindow()
      await appWindow.show()
      await appWindow.setFocus()
      isInTray.value = false
      console.log('[Tray] Window shown from tray')
    } catch (error) {
      console.error('[Tray] Failed to show window:', error)
    }
  }

  // 隐藏窗口到托盘
  const hideToTray = async () => {
    try {
      const appWindow = getCurrentWindow()
      await appWindow.hide()
      isInTray.value = true
      console.log('[Tray] Window hidden to tray')
    } catch (error) {
      console.error('[Tray] Failed to hide window to tray:', error)
    }
  }

  // 切换窗口显示/隐藏
  const toggleWindow = async () => {
    try {
      const appWindow = getCurrentWindow()
      const isVisible = await appWindow.isVisible()

      if (isVisible) {
        await hideToTray()
      } else {
        await showWindow()
      }
    } catch (error) {
      console.error('[Tray] Failed to toggle window:', error)
    }
  }

  // 退出应用
  const quitApp = async () => {
    try {
      console.log('[Tray] Quitting application...')
      // 先停止代理服务
      try {
        await invoke('plugin:pytauri|stop_proxy_for_shutdown')
      } catch (e) {
        console.debug('[Tray] Primary stop command failed, trying fallback:', e)
        // 尝试不带前缀的调用作为备选
        try {
          await invoke('stop_proxy_for_shutdown')
        } catch (e2) {
          console.warn('[Tray] Failed to stop proxy:', e2)
        }
      }

      // 等待一小段时间确保代理完全停止
      await new Promise(resolve => setTimeout(resolve, 500))

      // 退出应用 - 使用后端自定义命令 quit_app
      await invoke('quit_app')
    } catch (error) {
      console.error('[Tray] Failed to quit application:', error)
      // 如果出错，仍然尝试强制退出
      try {
        await invoke('quit_app')
      } catch (e) {
        console.error('[Tray] Force exit failed:', e)
      }
    }
  }

  // 检查是否应该以静默模式启动
  const checkSilentStart = async () => {
    try {
      const args = await invoke<boolean>('check_minimized_arg')
      if (args) {
        console.log('[Tray] Silent startup detected, hiding to tray')
        await hideToTray()
      }
    } catch (error) {
      console.error('[Tray] Failed to check startup args:', error)
    }
  }

  const init = async () => {
    if (import.meta.client) {
      // 延迟一点时间，确保应用完全就绪
      setTimeout(async () => {
        await createTray()
        await checkSilentStart()
      }, 500)
    }
  }

  return {
    isInTray,
    showWindow,
    hideToTray,
    toggleWindow,
    quitApp,
    init
  }
}

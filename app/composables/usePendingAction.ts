/**
 * 通用异步动作 pending 管理。
 * 同一时间只允许一个动作执行，用于按钮 loading / disabled 状态控制。
 */
export const usePendingAction = <T extends string>() => {
  const runningAction = ref<T | null>(null);

  const runAction = async (action: T, runner: () => Promise<boolean>) => {
    if (runningAction.value) {
      return false;
    }

    runningAction.value = action;
    try {
      return await runner();
    } finally {
      runningAction.value = null;
    }
  };

  return {
    runningAction,
    runAction,
  };
};

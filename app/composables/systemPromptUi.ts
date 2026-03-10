import type { SystemPromptItem } from "./mtgaTypes";

export const sortSystemPromptItemsByCreatedAt = (
  items: ReadonlyArray<SystemPromptItem>,
): SystemPromptItem[] => {
  return [...items].sort((a, b) => {
    const aTime = Date.parse(a.created_at);
    const bTime = Date.parse(b.created_at);
    if (Number.isNaN(aTime) || Number.isNaN(bTime)) {
      return b.created_at.localeCompare(a.created_at);
    }
    return bTime - aTime;
  });
};

export const formatSystemPromptCreatedAt = (value: string): string => {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toLocaleString("zh-CN", { hour12: false });
};

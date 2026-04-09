import * as vue from 'vue';
import { ElementTraceInfo } from './record.mjs';
export { PositionInfo, findTraceAtPointer, findTraceFromElement, findTraceFromVNode, getInternalStore, hasData, recordPosition } from './record.mjs';

interface EventsMap {
  [event: string]: any
}

interface DefaultEvents extends EventsMap {
  [event: string]: (...args: any) => void
}

interface Unsubscribe {
  (): void
}

interface Emitter<Events extends EventsMap = DefaultEvents> {
  /**
   * Calls each of the listeners registered for a given event.
   *
   * ```js
   * ee.emit('tick', tickType, tickDuration)
   * ```
   *
   * @param event The event name.
   * @param args The arguments for listeners.
   */
  emit<K extends keyof Events>(
    this: this,
    event: K,
    ...args: Parameters<Events[K]>
  ): void

  /**
   * Event names in keys and arrays with listeners in values.
   *
   * ```js
   * emitter1.events = emitter2.events
   * emitter2.events = { }
   * ```
   */
  events: Partial<{ [E in keyof Events]: Events[E][] }>

  /**
   * Add a listener for a given event.
   *
   * ```js
   * const unbind = ee.on('tick', (tickType, tickDuration) => {
   *   count += 1
   * })
   *
   * disable () {
   *   unbind()
   * }
   * ```
   *
   * @param event The event name.
   * @param cb The listener function.
   * @returns Unbind listener from event.
   */
  on<K extends keyof Events>(this: this, event: K, cb: Events[K]): Unsubscribe
}

declare const lastMatchedElement: vue.ShallowRef<ElementTraceInfo | undefined, ElementTraceInfo | undefined>;
interface Events {
    hover: (info: ElementTraceInfo | undefined, event: MouseEvent | PointerEvent) => void;
    click: (info: ElementTraceInfo, event: MouseEvent | PointerEvent) => void;
    enabled: () => void;
    disabled: () => void;
}
declare const events: Emitter<Events>;
declare const isEnabled: vue.Ref<boolean, boolean>;

export { ElementTraceInfo, events, isEnabled, lastMatchedElement };
export type { Events };

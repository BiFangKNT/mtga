import { toValue, isRef } from 'vue';

const VueResolver = (_, value) => {
  return isRef(value) ? toValue(value) : value;
};

export { VueResolver as V };

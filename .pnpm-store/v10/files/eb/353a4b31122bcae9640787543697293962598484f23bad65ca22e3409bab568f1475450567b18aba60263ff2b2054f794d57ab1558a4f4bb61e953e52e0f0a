import stack from './object.js';
import { addPrefix } from '../../functions/addPrefix.js';

export default ({ addComponents, prefix = '' }) => {
  const prefixedstack = addPrefix(stack, prefix);
  addComponents({ ...prefixedstack });
};

import toast from './object.js';
import { addPrefix } from '../../functions/addPrefix.js';

export default ({ addComponents, prefix = '' }) => {
  const prefixedtoast = addPrefix(toast, prefix);
  addComponents({ ...prefixedtoast });
};

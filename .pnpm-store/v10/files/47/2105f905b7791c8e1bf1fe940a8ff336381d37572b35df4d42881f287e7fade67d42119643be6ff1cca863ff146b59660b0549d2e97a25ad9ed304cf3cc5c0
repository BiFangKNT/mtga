import diff from './object.js';
import { addPrefix } from '../../functions/addPrefix.js';

export default ({ addComponents, prefix = '' }) => {
  const prefixeddiff = addPrefix(diff, prefix);
  addComponents({ ...prefixeddiff });
};

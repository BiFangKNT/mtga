import stat from './object.js';
import { addPrefix } from '../../functions/addPrefix.js';

export default ({ addComponents, prefix = '' }) => {
  const prefixedstat = addPrefix(stat, prefix);
  addComponents({ ...prefixedstat });
};

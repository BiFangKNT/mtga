import select from './object.js';
import { addPrefix } from '../../functions/addPrefix.js';

export default ({ addComponents, prefix = '' }) => {
  const prefixedselect = addPrefix(select, prefix);
  addComponents({ ...prefixedselect });
};

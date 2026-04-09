import fileinput from './object.js';
import { addPrefix } from '../../functions/addPrefix.js';

export default ({ addComponents, prefix = '' }) => {
  const prefixedfileinput = addPrefix(fileinput, prefix);
  addComponents({ ...prefixedfileinput });
};

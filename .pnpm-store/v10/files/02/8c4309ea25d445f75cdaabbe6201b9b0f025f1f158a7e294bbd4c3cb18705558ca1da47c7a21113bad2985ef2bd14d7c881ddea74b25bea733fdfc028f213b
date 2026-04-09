import join from './object.js';
import { addPrefix } from '../../functions/addPrefix.js';

export default ({ addUtilities, prefix = '' }) => {
  const prefixedjoin = addPrefix(join, prefix);
  addUtilities({ ...prefixedjoin });
};

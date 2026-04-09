import properties from './object.js';
import { addPrefix } from '../../functions/addPrefix.js';

export default ({ addBase, prefix = '' }) => {
  const prefixedproperties = addPrefix(properties, prefix);
  addBase({ ...prefixedproperties });
};

import validator from './object.js';
import { addPrefix } from '../../functions/addPrefix.js';

export default ({ addComponents, prefix = '' }) => {
  const prefixedvalidator = addPrefix(validator, prefix);
  addComponents({ ...prefixedvalidator });
};

import mockup from './object.js';
import { addPrefix } from '../../functions/addPrefix.js';

export default ({ addComponents, prefix = '' }) => {
  const prefixedmockup = addPrefix(mockup, prefix);
  addComponents({ ...prefixedmockup });
};

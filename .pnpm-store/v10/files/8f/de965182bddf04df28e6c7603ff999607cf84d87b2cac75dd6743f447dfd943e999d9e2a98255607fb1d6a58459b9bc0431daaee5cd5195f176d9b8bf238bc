import modal from './object.js';
import { addPrefix } from '../../functions/addPrefix.js';

export default ({ addComponents, prefix = '' }) => {
  const prefixedmodal = addPrefix(modal, prefix);
  addComponents({ ...prefixedmodal });
};

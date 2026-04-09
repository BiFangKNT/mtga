import steps from './object.js';
import { addPrefix } from '../../functions/addPrefix.js';

export default ({ addComponents, prefix = '' }) => {
  const prefixedsteps = addPrefix(steps, prefix);
  addComponents({ ...prefixedsteps });
};

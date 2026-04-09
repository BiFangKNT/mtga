import breadcrumbs from './object.js';
import { addPrefix } from '../../functions/addPrefix.js';

export default ({ addComponents, prefix = '' }) => {
  const prefixedbreadcrumbs = addPrefix(breadcrumbs, prefix);
  addComponents({ ...prefixedbreadcrumbs });
};

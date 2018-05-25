
import { createSelector } from 'reselect';

import {
  APISelector,
} from 'components/abstract/API';

export const APIConsumerActiveResourcesSelector = (api, consumer) => createSelector(
  APISelector(api),
  ({ consumers = {} } = {}) => consumers[consumer] && consumers[consumer].active,
);

export const a = 3;

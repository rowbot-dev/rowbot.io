
import { pick, isEmpty, mapValues } from 'lodash';
import { createSelector } from 'reselect';

export const APIsSelector = state => state.api;

export const APISelector = name => createSelector(
  APIsSelector,
  ({ [name]: api }) => api,
);

export const APIAuthenticationSelector = name => createSelector(
  APISelector(name),
  ({ authentication } = {}) => authentication,
);

export const APIDataSelector = name => createSelector(
  APISelector(name),
  ({ data } = {}) => data,
);

export const APISchemaSelector = (name, modelNames) => createSelector(
  APIDataSelector(name),
  ({ schema } = {}) => ((modelNames && !isEmpty(modelNames)) ? pick(schema, modelNames) : schema),
);

export const APIModelsSelector = (name, modelNames) => createSelector(
  APIDataSelector(name),
  ({ models } = {}) => ((modelNames && !isEmpty(modelNames)) ? pick(models, modelNames) : models),
);

export const APIFilteredDataSelector = (name, modelNames) => createSelector(
  APISchemaSelector(name, modelNames),
  APIModelsSelector(name, modelNames),
  (schema, models) => ({ schema, models }),
);

export const APISendersSelector = (name, senderName, senderNames) => createSelector(
  APISelector(name),
  ({ senders } = {}) => (
    (senderNames && !isEmpty(senderNames))
      ? pick(senders, senderNames)
      : pick(senders, [senderName])
  ),
);

export const APIConsumersSelector = name => createSelector(
  APISelector(name),
  ({ consumers } = {}) => consumers,
);

export const APIConsumerSelector = (name, consumerName) => createSelector(
  APIConsumersSelector(name),
  ({ [consumerName]: consumer } = {}) => (consumerName ? { [consumerName]: consumer } : {}),
);

export const APIFilteredSelector = (
  name,
  senderName,
  consumerName,
  senderNames,
  modelNames,
) => createSelector(
  APISelector(name),
  APIFilteredDataSelector(name, modelNames),
  APISendersSelector(name, senderName, senderNames),
  APIConsumerSelector(name, consumerName),
  (
    {
      data,
      senders,
      consumers,
      ...rest
    } = {},
    filteredData,
    filteredSenders,
    filteredConsumers,
  ) => ({
    data: filteredData,
    senders: filteredSenders,
    consumers: filteredConsumers,
    ...rest,
  }),
);

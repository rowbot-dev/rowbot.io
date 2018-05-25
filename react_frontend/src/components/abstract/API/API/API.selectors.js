
import { createSelector } from 'reselect';
import { APIConnector } from './API.connector';

export const APIsSelector = state => state.api;

export const APISelector = api => createSelector(
  APIsSelector,
  apis => apis[api],
);

export const APIConnection = api => createSelector(
  APISelector(api),
  API => new APIConnector(API),
);


import { createSelector } from 'reselect';

export const APIsSelector = state => state.api;

export const APISelector = api => createSelector(
  APIsSelector,
  apis => apis[api],
);

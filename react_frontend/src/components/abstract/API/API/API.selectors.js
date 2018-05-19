
import { createSelector } from 'reselect';

export const APIsSelector = state => state.api;

export const APISelector = api => state => state.api[api];

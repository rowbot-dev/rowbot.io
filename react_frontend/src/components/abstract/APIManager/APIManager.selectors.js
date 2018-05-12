
// import { createSelector } from 'reselect';

export const APIStatusSelector = state => state.api.status;

export const APIStatusAPISelector = api => state => state.api.status[api];

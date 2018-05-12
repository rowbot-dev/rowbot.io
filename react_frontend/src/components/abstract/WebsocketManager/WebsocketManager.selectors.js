
// import { createSelector } from 'reselect';

export const websocketStatusSelector = state => state.websockets.status;

export const websocketStatusSocketSelector = socket => state => state.websockets.status[socket];


import { createSelector } from 'reselect';

export const websocketSelector = socket => state => state.websockets[socket];

export const websocketStatusSelector = createSelector(
  websocketSelector,
  websocket => websocket.status,
);

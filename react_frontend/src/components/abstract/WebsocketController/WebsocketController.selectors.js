
import { createSelector } from 'reselect';

export const socketSelector = socket => state => state.websockets[socket];

export const messagesForSocket = socket => createSelector(
  [socketSelector(socket)],
  websocket => websocket && websocket.messages,
);

export const activeForSocket = socket => createSelector(
  [socketSelector(socket)],
  websocket => websocket && websocket.active,
);

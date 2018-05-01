
import { createSelector } from 'reselect';

export const websocketDataSelector = socket => state => state.websockets.data[socket];

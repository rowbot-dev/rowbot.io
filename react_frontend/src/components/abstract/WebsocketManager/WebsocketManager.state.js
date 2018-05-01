
import { compose } from 'redux';
import { connect } from 'react-redux';
import { merge } from 'lodash';

import WebsocketManager from './WebsocketManager';
import websocketManagerActionCreators from './WebsocketManager.actions';
import { websocketStatusSelector } from './WebsocketManager.selectors';

const mapStateToProps = (state, props) => {
  const status = websocketStatusSelector(state);
  const websockets = Object.keys(status)
    .filter(socket => status[socket].opening || status[socket].open)
    .map(socket => ({ socket, target: status[socket].target }));

  return {
    websockets,
  };
};

const mapDispatchToProps = {

};

export default compose(
  connect(mapStateToProps, mapDispatchToProps),
)(WebsocketManager);


import { compose } from 'redux';
import { connect } from 'react-redux';

import Websocket from './Websocket';
import websocketActionCreators from './Websocket.actions';
import { websocketStatusSocketSelector } from '../WebsocketManager.selectors';
import { websocketDataSelector } from './Websocket.selectors';

const mapStateToProps = (state, { id: socket }) => {
  const status = websocketStatusSocketSelector(socket);
  const data = websocketDataSelector(socket);

  return {
    status: status(state),
    data: data(state),
    // authentication: authenticationSelector(state),
  };
};

const mapDispatchToProps = {
  ...websocketActionCreators,
};

export default compose(
  connect(mapStateToProps, mapDispatchToProps),
)(Websocket);

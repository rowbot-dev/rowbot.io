
import { compose } from 'redux';
import { connect } from 'react-redux';

import Websocket from './Websocket';
import websocketActionCreators from './Websocket.actions';
import { websocketSelector } from './Websocket.selectors';

const mapStateToProps = (state, { id: socket }) => {
  const data = websocketSelector(socket);

  return {
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

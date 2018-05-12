
import { compose } from 'redux';
import { connect } from 'react-redux';

import WebsocketManager from './WebsocketManager';
import { websocketStatusSelector } from './WebsocketManager.selectors';

const mapStateToProps = (state, props) => {
  const status = websocketStatusSelector(state);
  const websockets = Object.keys(status)
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

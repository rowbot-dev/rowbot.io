
import { compose } from 'redux';
import { connect } from 'react-redux';

import WebsocketController from './WebsocketController'
import websocketControllerActionCreators from './WebsocketController.actions';
import { socketIsOpen, socketShouldReopen, messagesForSocket, activeForSocket } from './WebsocketController.selectors';

const mapStateToProps = (state, { id: socket }) => {
  const open = socketIsOpen(socket);
  const reopen = socketShouldReopen(socket);
  const messages = messagesForSocket(socket);
  const active = activeForSocket(socket);

  return {
    open: open(state),
    reopen: reopen(state),
    messages: messages(state),
    active: active(state),
  };
};

const mapDispatchToProps = {
  onOpenWebsocket: websocketControllerActionCreators.openWebsocket,
  onConsumeWebsocketMessage: websocketControllerActionCreators.consumeWebsocketMessage,
  onConsumeWebsocketMessageSuccess: websocketControllerActionCreators.consumeWebsocketMessageSuccess,
  onReceiveWebsocketMessage: websocketControllerActionCreators.receiveWebsocketMessage,
  onCloseWebsocket: websocketControllerActionCreators.closeWebsocket,
  onWebsocketError: websocketControllerActionCreators.websocketError,
};

export default compose(
  connect(mapStateToProps, mapDispatchToProps),
)(WebsocketController);

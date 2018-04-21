
import React, { Component } from 'react';

import { compose } from 'redux';
import { connect } from 'react-redux';

import websocketControllerActionCreators from 'components/abstract/WebsocketController/WebsocketController.actions';
import { messagesForSocket, activeForSocket } from 'components/abstract/WebsocketController/WebsocketController.selectors';
import uuid from 'util/uuid';

class MessageButton extends Component {

  constructor () {
    super();

    this.handleClick = this.handleClick.bind(this);
  }

  handleClick () {
    const { onSendWebsocketMessage } = this.props;

    onSendWebsocketMessage('api', uuid(), { hello: 'hello back' });
  }

  render () {
    return (
      <button onClick={this.handleClick}>Hello</button>
    );
  }
}

const mapStateToProps = (state) => {

  const messages = messagesForSocket('api');
  const active = activeForSocket('api');

  return {
    messages: messages(state),
    active: active(state),
  };
};

const mapDispatchToProps = {
  onSendWebsocketMessage: websocketControllerActionCreators.sendWebsocketMessage,
  onReceiveWebsocketMessage: websocketControllerActionCreators.receiveWebsocketMessage,
};

export default compose(
  connect(mapStateToProps, mapDispatchToProps),
)(MessageButton);

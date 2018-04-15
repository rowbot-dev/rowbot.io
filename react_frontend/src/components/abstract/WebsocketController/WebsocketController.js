
import { Component } from 'react';
import PropTypes from 'prop-types';

import uuid from 'util/uuid';
import { encode, decode } from './util';

class WebsocketController extends Component {

  constructor (props) {
    super();
  }

  componentDidMount () {
    this.open();
  }

  componentWillUnmount () {
    this.close();
  }

  open () {
    const { target } = this.props;

    if (!this.socket) {
      this.socket = new WebSocket(target);
      this.socket.onopen = this.handleOpen.bind(this);
      this.socket.onmessage = this.handleMessage.bind(this);
      this.socket.onclose = this.handleClose.bind(this);
      this.socket.onerror = this.handleError.bind(this);
    }
  }

  close () {
    if (this.socket) {
      this.socket.close(3001);
      this.socket = null;
    }
  }

  send (message) {
    const { id, onSendWebsocketMessage } = this.props;

    if (this.socket) {
      const messageID = uuid();

      this.socket.send(encode({
        id: messageID,
        content: message,
      }));

      onSendWebsocketMessage(id, messageID, message);
    }
  }

  handleOpen () {
    const { id, onOpenWebsocket } = this.props;

    onOpenWebsocket(id);
  }

  handleMessage (message) {
    const { id, onReceiveWebsocketMessage } = this.props;

    const { id: messageID, data } = message;

    onReceiveWebsocketMessage(id, messageID, data);
  }

  handleClose (event) {
    const { id, target, onCloseWebsocket } = this.props;

    if (event.code === 3001) {
      console.log('Closed', target);
    } else {
      console.log('Unable to connected to', target);
    }

    onCloseWebsocket(id);
  }

  handleError (event) {
    const { id, onWebsocketError } = this.props;

    if (this.socket && this.socket.readyState === 1) {

    }

    onWebsocketError(id);
  }

  render () {
    return null;
  }

}

export default WebsocketController;

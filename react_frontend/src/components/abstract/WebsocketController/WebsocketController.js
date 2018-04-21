
import { isEmpty } from 'lodash';
import { Component } from 'react';
import PropTypes from 'prop-types';

import uuid from 'util/uuid';
import { encode, decode } from './WebsocketController.util';

class WebsocketController extends Component {

  constructor (props) {
    super();

    this.state = {
      active: null,
    };
  }

  componentDidMount () {
    this.open();
  }

  componentDidUpdate (prevProps) {
    const { active: prevActive } = prevProps;
    const { id, onConsumeWebsocketMessage, active: nextActive, messages: nextMessages } = this.props;

    const shouldConsume = !isEmpty(nextMessages) && !nextActive;

    if (shouldConsume) {
      onConsumeWebsocketMessage(id);
    }

    const shouldSend = (
      nextActive &&
      nextActive !== prevActive
    );

    if (shouldSend) {
      this.send();
    }
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

  send () {
    const { id, messages, active, onConsumeWebsocketMessageSuccess } = this.props;

    if (this.socket) {
      try {
        this.socket.send(encode({
          socket: id,
          id: active,
          content: messages[active].message,
        }));
        onConsumeWebsocketMessageSuccess(id, active);
      } catch (error) {
        this.handleError(id, active);
      }
    }
  }

  handleOpen () {
    const { id, onOpenWebsocket } = this.props;

    onOpenWebsocket(id);
  }

  handleMessage (message) {
    const { id, onReceiveWebsocketMessage } = this.props;

    const { id: messageID, data } = decode(message.data);

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
    const { id, active, onWebsocketError } = this.props;

    if (this.socket && this.socket.readyState === 1) {

    }

    onWebsocketError(id, active);
  }

  render () {
    return null;
  }

}

WebsocketController.defaultProps = {
  active: null,
  messages: null,
};

WebsocketController.propTypes = {
  active: PropTypes.string,
  messages: PropTypes.object,
};

export default WebsocketController;

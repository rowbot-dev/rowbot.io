
import { isEmpty } from 'lodash';
import { Component } from 'react';
import PropTypes from 'prop-types';

import uuid from 'util/uuid';
import { encode, decode } from './Websocket.util';

class Websocket extends Component {

  componentDidMount () {
    this.open();
  }

  componentDidUpdate (prevProps) {
    const { status: { reopen: prevReopen } = {}, data: { active: prevActive } = {} } = prevProps;
    const {
      id,
      onWebsocketConsume,
      status: { reopen, closed },
      data: { active: nextActive, messages: { length: numberOfMessages } = [] } = {},
    } = this.props;

    const shouldConsume = numberOfMessages > 0;

    if (shouldConsume) {
      onWebsocketConsume(id);
    }

    const shouldSend = nextActive && nextActive !== prevActive;

    if (shouldSend) {
      this.send();
    }

    const shouldAttemptReopen = closed && reopen && reopen !== prevReopen;

    if (shouldAttemptReopen) {
      this.attemptReopen();
    }
  }

  componentWillUnmount () {
    this.close();
    clearInterval(this.attempt_reopen_interval);
  }

  open () {
    const { target } = this.props;

    this.socket = new WebSocket(target);
    this.socket.onopen = this.handleOpen.bind(this);
    this.socket.onmessage = this.handleMessage.bind(this);
    this.socket.onclose = this.handleClose.bind(this);
    this.socket.onerror = this.handleError.bind(this);
  }

  attemptReopen () {
    this.attempt_reopen_interval = window.setInterval(
      () => this.props.status.reopen && this.open(),
      1000,
    );
  }

  close () {
    if (this.socket) {
      this.socket.close(3001);
      this.socket = null;
    }
  }

  send () {
    const { id, data: { active, consumed }, authentication } = this.props;

    if (this.socket) {
      try {
        this.socket.send(encode({
          context: {
            socket: id,
            message: active,
            ...authentication,
          },
          data: consumed[active],
        }));
      } catch (error) {
        this.handleError();
      }
    }
  }

  handleOpen () {
    const { id, onWebsocketOpen } = this.props;

    onWebsocketOpen(id);
  }

  handleMessage (message) {
    const { id, onWebsocketReceive } = this.props;

    const { id: messageID, data } = decode(message.data);

    onWebsocketReceive(id, messageID, data);
  }

  handleClose (event) {
    const { id, target, onWebsocketClose } = this.props;

    let reopen = false;
    if (event.code === 3001) {
      console.warn('Closed', target);
    } else {
      reopen = true;
      console.warn('Unable to connected to', target);
    }

    onWebsocketClose(id, reopen);
  }

  handleError (event) {
    const { id, active, onWebsocketError } = this.props;

    if (this.socket && this.socket.readyState === 1) {
      onWebsocketError(id, active);
    }
  }

  render () {
    return null;
  }

}

// Websocket.defaultProps = {
//   active: null,
//   messages: null,
// };
//
// Websocket.propTypes = {
//   active: PropTypes.object,
//   messages: PropTypes.object,
// };

export default Websocket;

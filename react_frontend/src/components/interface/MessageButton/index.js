
import React, { Component } from 'react';

import { compose } from 'redux';
import { connect } from 'react-redux';

import { websocketActionCreators } from 'components/abstract/WebsocketManager';
import uuid from 'util/uuid';

class MessageButton extends Component {

  constructor () {
    super();

    this.handleClick = this.handleClick.bind(this);
  }

  handleClick () {
    const { registerWebsocketMessage } = this.props;

    registerWebsocketMessage(
      'api',
      uuid(),
      {
        schema: true,
        request: {
          Member: {
            filter: {},
          },
        },
      },
    );
  }

  render () {
    return (
      <button onClick={this.handleClick}>Hello</button>
    );
  }
}

const mapStateToProps = (state) => {
  return {};
};

const mapDispatchToProps = {
  registerWebsocketMessage: websocketActionCreators.onWebsocketRegister,
};

export default compose(
  connect(mapStateToProps, mapDispatchToProps),
)(MessageButton);

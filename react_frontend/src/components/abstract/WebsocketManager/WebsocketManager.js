
import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';

import uuid from 'util/uuid';

import Websocket from './Websocket';

class WebsocketManager extends Component {

  constructor (props) {
    super();

  }

  componentDidMount () {

  }

  componentDidUpdate (prevProps) {

  }

  render () {
    const { websockets } = this.props;

    return (
      <Fragment>
        {websockets.map((websocket, index) => {
          const { socket, target } = websocket;

          return <Websocket id={socket} target={target} key={socket} />;
        })}
      </Fragment>
    );
  }

}

WebsocketManager.defaultProps = {

};

WebsocketManager.propTypes = {

};

export default WebsocketManager;

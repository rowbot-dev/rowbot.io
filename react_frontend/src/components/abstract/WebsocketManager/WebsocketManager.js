
import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';

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

WebsocketManager.propTypes = {
  websockets: PropTypes.array.isRequired,
};

export default WebsocketManager;


import { isEmpty } from 'lodash';
import React, { Component } from 'react';
import PropTypes from 'prop-types';

import uuid from 'util/uuid';
import Websocket from 'components/abstract/Websocket';

class API extends Component {

  componentDidMount () {
    const { id, target, onAPICreated } = this.props;

    onAPICreated(id, target);
  }

  componentDidUpdate (prevProps) {
    const {
      api: { schema: prevSchema } = {},
    } = prevProps;
    const {
      id,
      api: { schema },
    } = this.props;

    
  }

  render () {
    const { id, target } = this.props;
    const [protocol] = target.split('://');

    if (protocol === 'ws') {
      return (
        <Websocket id={id} target={target} />
      );
    }

    return null;
  }

  componentWillUnmount () {
    const { id, onAPIDestroyed } = this.props;

    onAPIDestroyed(id);
  }

}

API.defaultProps = {

};

API.propTypes = {

};

export default API;

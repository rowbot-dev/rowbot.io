
import React, { Component } from 'react';
import PropTypes from 'prop-types';

import Websocket from 'components/abstract/Websocket';

class API extends Component {

  componentWillMount () {
    const { id, target, onAPICreated } = this.props;

    onAPICreated(id, target);
  }

  componentWillUnmount () {
    const { id, onAPIDestroyed } = this.props;

    onAPIDestroyed(id);
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

}

API.defaultProps = {

};

API.propTypes = {
  id: PropTypes.string.isRequired,
  target: PropTypes.string.isRequired,
  onAPICreated: PropTypes.func.isRequired,
  onAPIDestroyed: PropTypes.func.isRequired,
};

export default API;

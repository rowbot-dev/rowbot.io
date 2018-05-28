
import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';
import { Input } from 'semantic-ui-react';

import constants from 'rowbot/constants';
import { withAPI } from 'components/abstract/API';

class APIConnectedInput extends Component {

  constructor () {
    super();

    this.handleInput = this.handleInput.bind(this);
  }

  handleInput (event, data) {
    const { api: { [constants.ROWBOT]: rowbot } } = this.props;
    const { value } = data;

    rowbot.setSenderValue(value);
  }

  render () {
    return (
      <Fragment>
        <Input onChange={this.handleInput} />
      </Fragment>
    );
  }

}

APIConnectedInput.propTypes = {
  ...withAPI.propTypes,
};

export default APIConnectedInput;

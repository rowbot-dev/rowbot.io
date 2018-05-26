
import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';
import { Input } from 'semantic-ui-react';

import constants from 'rowbot/constants';
import { withAPI } from 'components/abstract/API';

class APIConnectedList extends Component {

  constructor () {
    super();

    this.handleInput = this.handleInput.bind(this);
  }

  handleInput (event, data) {
    const { api: { [constants.ROWBOT]: rowbot } } = this.props;
    const { models: { Member } } = rowbot;

    const { value } = data;

    Member.filter({
      name__contains: value,
    });
  }

  render () {
    const { api: { [constants.ROWBOT]: rowbot } } = this.props;
    const { models: { Member } } = rowbot;

    return (
      <Fragment>
        <Input onChange={this.handleInput} />
      </Fragment>
    );
  }

}

APIConnectedList.propTypes = {
  ...withAPI.propTypes,
};

export default APIConnectedList;

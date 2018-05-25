
import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';
import { Input } from 'semantic-ui-react';

import { withAPI } from 'components/abstract/API';

const ROWBOT = 'rowbot';

class APIConnectedList extends Component {

  constructor () {
    super();

    this.handleInput = this.handleInput.bind(this);
  }

  handleInput (event, data) {
    const { api } = this.props;
    const { models: { Member } } = api[ROWBOT];

    const { value } = data;

    Member.filter({
      name__contains: value,
    });
  }

  render () {
    const { api } = this.props;

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

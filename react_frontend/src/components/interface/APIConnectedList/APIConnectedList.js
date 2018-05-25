
import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';
import { Input } from 'semantic-ui-react';

class APIConnectedList extends Component {

  constructor () {
    super();

    this.handleInput = this.handleInput.bind(this);
  }

  handleInput (event, data) {
    const { models: { Member } } = this.props;
    const { value } = data;

    Member.filter({

    });
  }

  render () {
    return (
      <Fragment>
        <Input onChange={this.handleInput} />
      </Fragment>
    );
  }

}

APIConnectedList.propTypes = {

};

export default APIConnectedList;

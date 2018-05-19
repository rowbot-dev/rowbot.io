
import React, { Component } from 'react';
import { merge } from 'lodash';
import { compose } from 'redux';
import { connect } from 'react-redux';

import uuid from 'util/uuid';

class MessageButton extends Component {

  constructor () {
    super();

    this.handleClick = this.handleClick.bind(this);
  }

  handleClick () {
    const { models: { Member } } = this.props;

    Member.remote.filter();
  }

  render () {
    return (
      <button onClick={this.handleClick}>Hello</button>
    );
  }
}

const mapStateToProps = state => {
  return {
    // models,
  };
};

const mapDispatchToProps = {

};

export default compose(
  // withAPI('api', uiud()),
  connect(mapStateToProps, mapDispatchToProps),
)(MessageButton);

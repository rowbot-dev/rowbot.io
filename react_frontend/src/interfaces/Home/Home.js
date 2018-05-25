
import React, { Component } from 'react';
import PropTypes from 'prop-types';

import APIConnectedList from 'components/interface/APIConnectedList';

class Home extends Component {

  componentDidMount () {
    const { createAPI } = this.props;

    createAPI('rowbot', 'ws://localhost:8000/api/');
  }

  render () {
    return (
      <APIConnectedList />
    );
  }

}

Home.propTypes = {
  createAPI: PropTypes.func.isRequired,
};

export default Home;

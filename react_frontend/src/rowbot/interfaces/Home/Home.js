
import React, { Component } from 'react';
import PropTypes from 'prop-types';

import APIConnectedList from 'rowbot/components/interface/APIConnectedList';

class Home extends Component {

  componentDidMount () {

  }

  render () {
    return (
      <APIConnectedList />
    );
  }

}

Home.propTypes = {

};

export default Home;

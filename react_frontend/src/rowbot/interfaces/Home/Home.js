
import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';

import APIConnectedList from 'rowbot/components/interface/APIConnectedList';
import APIConnectedInput from 'rowbot/components/interface/APIConnectedInput';

class Home extends Component {

  componentDidMount () {

  }

  render () {
    return (
      <Fragment>
        <APIConnectedList />
        <APIConnectedInput />
      </Fragment>
    );
  }

}

Home.propTypes = {

};

export default Home;

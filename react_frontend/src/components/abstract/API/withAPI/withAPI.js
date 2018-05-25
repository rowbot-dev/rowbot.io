
import React, { Component } from 'react';
import PropTypes from 'prop-types';

const withAPI = (api, consumer) => WrappedComponent => {
  class WithAPI extends Component {

    componentDidMount () {

    }

    render () {
      return <WrappedComponent {...this.props} />;
    }

  }

  WithAPI.propTypes = {
    
  };

  return WithAPI;
};

export default withAPI;

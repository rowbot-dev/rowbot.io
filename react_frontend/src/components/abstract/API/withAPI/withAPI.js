
import React, { Component } from 'react';
import PropTypes from 'prop-types';

const withAPI = connector => WrappedComponent => {
  class WithAPI extends Component {

    componentWillMount () {
      connector.register(this.props);
    }

    componentDidUpdate () {
      connector.didUpdate();
    }

    render () {
      return <WrappedComponent {...connector.connect(this.props)} />;
    }

  }

  WithAPI.propTypes = {

  };

  return WithAPI;
};

export default withAPI;


import React, { Component } from 'react';
import PropTypes from 'prop-types';

const withAPI = (api, consumer) => WrappedComponent => {
  class WithAPI extends Component {

    componentDidMount () {
      const { onAPIConsumerRegister } = this.props;

      onAPIConsumerRegister(api, consumer);
    }

    render () {
      return <WrappedComponent {...this.props} />;
    }

  }

  WithAPI.propTypes = {
    onAPIConsumerRegister: PropTypes.func.isRequired,
  };

  return WithAPI;
};

export default withAPI;

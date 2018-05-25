
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connectAPI } from './withAPI.connector';

const withAPI = (api, consumer) => WrappedComponent => {
  class WithAPI extends Component {

    componentDidMount () {
      const { onAPIConsumerRegister } = this.props;

      onAPIConsumerRegister(api, consumer);
    }

    render () {
      const {
        onAPIConsumerRegister,
        onAPIConsumerReferenceAdd,
      } = this.props;
      const connectedProps = connectAPI(
        api,
        consumer,
        this.props,
        {
          register: onAPIConsumerRegister,
          add: onAPIConsumerReferenceAdd,
        },
      );

      return <WrappedComponent {...connectedProps} />;
    }

  }

  WithAPI.propTypes = {
    api: PropTypes.object.isRequired,
    onAPIConsumerRegister: PropTypes.func.isRequired,
    onAPIConsumerReferenceAdd: PropTypes.func.isRequired,
  };

  return WithAPI;
};

export default withAPI;


import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';

import API from '../API';

class APIManager extends Component {

  constructor (props) {
    super();

  }

  render () {
    const { apis } = this.props;

    return (
      <Fragment>
        {Object.keys(apis).map(id => {
          const { status: { target } } = apis[id];

          return <API id={id} target={target} key={id} />;
        })}
      </Fragment>
    );
  }

}

APIManager.defaultProps = {

};

APIManager.propTypes = {
  apis: PropTypes.object.isRequired,
};

export default APIManager;

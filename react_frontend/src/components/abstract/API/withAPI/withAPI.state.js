
import { compose } from 'redux';
import { connect } from 'react-redux';
import { merge } from 'lodash';

import { APIConnector } from './withAPI.connector';
import withAPI from './withAPI';

const mapStateToProps = connector => (state, props) => merge(
  {},
  props,
  {
    api: {
      ...connector.select(state),
    },
  },
);

export default options => {
  const connector = new APIConnector(options);
  return compose(
    connect(mapStateToProps(connector)),
    withAPI(connector),
  );
};

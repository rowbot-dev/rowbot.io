
import { compose } from 'redux';
import { connect } from 'react-redux';
import { merge } from 'lodash';

import { APIConnection } from 'components/abstract/API/';
import withAPI from './withAPI';
import withAPIActionCreators from './withAPI.actions';

const mapStateToProps = (api, consumer) => (state, props) => {
  const connection = APIConnection(api);

  return merge(
    {},
    props,
    {
      api: {
        [api]: connection(state),
      }
    },
  );
};

export default (api, consumer) => compose(
  connect(mapStateToProps(api, consumer)),
  withAPI(api, consumer),
);

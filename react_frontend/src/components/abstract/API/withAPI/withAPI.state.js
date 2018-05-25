
import { compose } from 'redux';
import { connect } from 'react-redux';
import { merge } from 'lodash';

import withAPI from './withAPI';
import withAPIActionCreators from './withAPI.actions';
import { APIConsumerActiveResourcesSelector } from './withAPI.selectors';

const mapStateToProps = (api, consumer) => (state, props) => {
  return merge(
    {},
    props,
    {
      api: API(state),
    },
  );
};

const mapDispatchToProps = (api, consumer) => ({
  ...withAPIActionCreators,
});

export default (api, consumer) => compose(
  connect(mapStateToProps(api, consumer), mapDispatchToProps(api, consumer)),
  withAPI(api, consumer),
);

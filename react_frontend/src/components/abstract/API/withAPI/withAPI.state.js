
import { compose } from 'redux';
import { connect } from 'react-redux';
import { merge } from 'lodash';

import { APISelector } from '../API.selectors';
import withAPI from './withAPI';
import withAPIActionCreators from './withAPI.actions';

const mapStateToProps = api => (state, props) => {
  const API = APISelector(api);

  return merge(
    {},
    props,
    {
      api: {
        [api]: API(state),
      },
    },
  );
};

const mapDispatchToProps = {
  ...withAPIActionCreators,
};

export default (api, consumer) => compose(
  connect(mapStateToProps(api), mapDispatchToProps),
  withAPI(api, consumer),
);


import { compose } from 'redux';
import { connect } from 'react-redux';

import APIManager from './APIManager';
// import APIManagerActionCreators from './APIManager.actions';
import { APIStatusSelector } from './APIManager.selectors';

const mapStateToProps = (state, props) => {
  const status = APIStatusSelector(state);
  const apis = Object.keys(status)
    .filter(api => status[api].creating || status[api].created)
    .map(api => ({ api, target: status[api].target }));

  return {
    apis,
  };
};

const mapDispatchToProps = {

};

export default compose(
  connect(mapStateToProps, mapDispatchToProps),
)(APIManager);

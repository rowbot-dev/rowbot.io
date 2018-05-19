
import { compose } from 'redux';
import { connect } from 'react-redux';

import { websocketSelector } from 'components/abstract/Websocket';
import API from './API';
import APIActionCreators from './API.actions';
import { APISelector } from './API.selectors';

const mapStateToProps = (state, { id }) => {
  const api = APISelector(id);

  return {
    api: api(state),
  };
};

const mapDispatchToProps = {
  ...APIActionCreators,
};

export default compose(
  connect(mapStateToProps, mapDispatchToProps),
)(API);

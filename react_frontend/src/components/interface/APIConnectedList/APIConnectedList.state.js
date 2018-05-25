
import { compose } from 'redux';
import { connect } from 'react-redux';

import { withAPI } from 'components/abstract/API';
import APIConnectedList from './APIConnectedList';

const mapStateToProps = state => {
  return {

  };
};

const mapDispatchToProps = {

};

export default compose(
  connect(mapStateToProps, mapDispatchToProps),
  withAPI('rowbot', 'api-connected-list'),
)(APIConnectedList);

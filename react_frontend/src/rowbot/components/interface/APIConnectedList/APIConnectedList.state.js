
import { compose } from 'redux';
import { connect } from 'react-redux';

import constants from 'rowbot/constants';
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
  withAPI({
    name: constants.ROWBOT,
    consumer: 'api-connected-list',
    senders: ['api-connected-input'],
    models: ['Member'],
  }),
)(APIConnectedList);

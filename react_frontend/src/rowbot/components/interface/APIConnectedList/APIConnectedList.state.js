
import { compose } from 'redux';
import { connect } from 'react-redux';

import constants, { senders, consumers, models } from 'rowbot/constants';
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
    consumer: consumers.API_CONNECTED_LIST,
    senders: [senders.API_CONNECTED_INPUT],
    models: [models.MEMBER, models.ASSET],
  }),
)(APIConnectedList);


import { compose } from 'redux';
import { connect } from 'react-redux';

import constants from 'rowbot/constants';
import { withAPI } from 'components/abstract/API';
import APIConnectedInput from './APIConnectedInput';

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
    sender: 'api-connected-input',
    models: ['Member'],
  }),
)(APIConnectedInput);

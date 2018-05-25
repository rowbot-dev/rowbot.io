
import { compose } from 'redux';
import { connect } from 'react-redux';

import APIManager from './APIManager';
import { APIsSelector } from '../API.selectors';

const mapStateToProps = state => ({
  apis: APIsSelector(state),
});

const mapDispatchToProps = {

};

export default compose(
  connect(mapStateToProps, mapDispatchToProps),
)(APIManager);
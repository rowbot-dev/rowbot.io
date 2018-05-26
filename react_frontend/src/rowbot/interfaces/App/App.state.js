
import { compose } from 'redux';
import { connect } from 'react-redux';

import { APIManagerActionCreators } from 'components/abstract/API';

import App from './App.style';

const mapStateToProps = state => ({});

const mapDispatchToProps = {
  ...APIManagerActionCreators,
};

export default compose(
  connect(mapStateToProps, mapDispatchToProps),
)(App);

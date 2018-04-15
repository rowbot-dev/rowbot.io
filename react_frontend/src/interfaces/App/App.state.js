import { compose } from 'redux';
import { connect } from 'react-redux';

import App from './App.style';

export default compose(
  connect(),
)(App);

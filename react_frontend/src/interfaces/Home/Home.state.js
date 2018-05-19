
import { compose } from 'redux';
import { connect } from 'react-redux';

import { APIManagerActionCreators } from 'components/abstract/API';

import Home from './Home.style';

const mapStateToProps = (state, props) => {


  return {

  };
};

const mapDispatchToProps = {
  ...APIManagerActionCreators,
};

export default compose(
  connect(mapStateToProps, mapDispatchToProps),
)(Home);

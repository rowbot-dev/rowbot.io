
import { compose } from 'redux';
import { connect } from 'react-redux';

import { websocketManagerActionCreators } from 'components/abstract/WebsocketManager';

import Home from './Home.style';

const mapStateToProps = (state, props) => {


  return {

  };
};

const mapDispatchToProps = {
  openWebsocket: websocketManagerActionCreators.openWebsocket,
};

export default compose(
  connect(mapStateToProps, mapDispatchToProps),
)(Home);

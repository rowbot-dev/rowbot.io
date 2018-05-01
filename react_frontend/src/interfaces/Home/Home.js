
import React, { Component } from 'react';

import MessageButton from 'components/interface/MessageButton';

class Home extends Component {

  componentDidMount () {
    const { openWebsocket } = this.props;

    openWebsocket('api', 'ws://localhost:8000/api/');
  }

  render () {
    return (
      <MessageButton />
    );
  }
}

Home.propTypes = {

};

export default Home;

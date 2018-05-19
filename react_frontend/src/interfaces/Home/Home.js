
import React, { Component } from 'react';

import MessageButton from 'components/interface/MessageButton';

class Home extends Component {

  componentDidMount () {
    const { createAPI } = this.props;

    createAPI('rowbot', 'ws://localhost:8000/api/');
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


import React, { Component } from 'react';
import PropTypes from 'prop-types';

import Home from 'rowbot/interfaces/Home';
import { APIManager } from 'components/abstract/API';

// <ActionManager />
// <SceneManager />
// <RouteManager />

// <Authentication />
// <Dashboard />
// <Events />
// <Members />
// <Clubs />
// <Teams />
// <Assets />

class App extends Component {

  componentDidMount () {
    const { createAPI } = this.props;

    createAPI('rowbot', 'ws://localhost:8000/api/');
  }

  render () {
    return (
      <main>
        <APIManager />

        <Home />
      </main>
    );
  }

}

App.propTypes = {
  createAPI: PropTypes.func.isRequired,
};

export default App;

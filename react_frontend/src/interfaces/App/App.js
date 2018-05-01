
import React from 'react';

import Home from 'interfaces/Home';

import WebsocketManager from 'components/abstract/WebsocketManager';
import APIManager from 'components/abstract/APIManager';

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

const App = () => {
  return (
    <main>
      <WebsocketManager />
      <APIManager />

      <Home />
    </main>
  );
};

export default App;

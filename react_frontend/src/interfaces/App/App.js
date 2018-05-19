
import React from 'react';

import Home from 'interfaces/Home';

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

const App = () => {
  return (
    <main>
      <APIManager />

      <Home />
    </main>
  );
};

export default App;

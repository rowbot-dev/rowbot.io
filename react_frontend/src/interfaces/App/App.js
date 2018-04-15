
import React from 'react';

import WebsocketController, { API } from 'components/abstract/WebsocketController';

const App = () => {
  return (
    <main>
      <WebsocketController id={API} target='ws://localhost:8000/api/' />
    </main>
  );
};

export default App;

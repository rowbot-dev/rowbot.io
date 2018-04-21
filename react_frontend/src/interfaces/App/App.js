
import React from 'react';

import WebsocketController from 'components/abstract/WebsocketController';
import MessageButton from 'components/interface/MessageButton';

const App = () => {
  return (
    <main>
      <WebsocketController id='api' target='ws://localhost:8000/api/' />
      <MessageButton />
    </main>
  );
};

export default App;

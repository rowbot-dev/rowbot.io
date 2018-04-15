import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { BrowserRouter as Router } from 'react-router-dom';

import App from 'interfaces/App';
import Store from 'store/Store';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(
  <Provider store={Store}>
    <Router>
      <App />
    </Router>
  </Provider>,
  document.getElementById('root')
);

registerServiceWorker();

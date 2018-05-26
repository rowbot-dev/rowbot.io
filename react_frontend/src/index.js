
import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';

import Store from 'store/Store';
import App from 'rowbot/interfaces/App';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(
  <Provider store={Store}>
    <App />
  </Provider>,
  document.getElementById('root'),
);

registerServiceWorker();


import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';

import App from 'interfaces/App';
import Store from 'store/Store';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(
  <Provider store={Store}>
    <App />
  </Provider>,
  document.getElementById('root'),
);

registerServiceWorker();

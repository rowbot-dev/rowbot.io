
import { Component } from 'react';

import constants, { senders, models } from 'rowbot/constants';
import { withAPI } from 'components/abstract/API';

class APIConnectedList extends Component {

  componentDidUpdate () {
    const { api: { [constants.ROWBOT]: rowbot } } = this.props;

    rowbot.setConsumerConverter(({
      senders: {
        [senders.API_CONNECTED_INPUT]: apiConnectedInputValue,
      },
      models: {
        [models.MEMBER]: Member,
      },
    }) => ([
      Member.filter({
        username__contains: apiConnectedInputValue,
      }),
    ]));
  }

  render () {
    return null;
  }

}

APIConnectedList.propTypes = {
  ...withAPI.propTypes,
};

export default APIConnectedList;

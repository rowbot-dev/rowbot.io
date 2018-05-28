
import { Component } from 'react';

import constants from 'rowbot/constants';
import { withAPI } from 'components/abstract/API';

class APIConnectedList extends Component {

  componentDidUpdate () {
    const { api: { [constants.ROWBOT]: rowbot } } = this.props;
    const { models: { Member } } = rowbot;

    if (Member) {
      Member.filter(value => ({
        name__contains: value,
      }));
    }
  }

  render () {
    return null;
  }

}

APIConnectedList.propTypes = {
  ...withAPI.propTypes,
};

export default APIConnectedList;

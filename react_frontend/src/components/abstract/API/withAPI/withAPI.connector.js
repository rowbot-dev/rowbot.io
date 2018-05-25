
import { mapValues, merge, pick, omit } from 'lodash';
import uuid from 'util/uuid';

export const types = {

};

class Instance {

  constructor () {

  }

  fetch () {

  }

  save () {

  }

  delete () {

  }

}

class Model {

  constructor (api, modelName, model) {
    this.api = api;
    this.name = modelName;

    const { attributes, methods, relationships } = model;
  }

  create (args) {

  }

  filter (args) {
    // 1. Make new unique identifier
    const identifier = uuid();

    // 2. dispatch action registering unique identifier with args and consumer
    const { api, consumer, actions: { add } } = this.api;

    add(
      api,
      consumer,
      identifier,
      {
        models: {
          [this.name]: {
            filter: args,
          },
        },
      },
    );
    // withAPIActionCreators.onAPIConsumerReferenceAdd(api, consumer, identifier, args);
  }

  get () {

  }

  run (args) {

  }

}

export class APIConnector {

  constructor (api, consumer, state = {}, actions) {
    this.api = api;
    this.consumer = consumer;
    this.actions = actions;

    const { data: { schema } = {} } = state;

    this.models = mapValues(schema, (model, modelName) => new Model(this, modelName, model));
  }

  destroy () {

  }

}

export function connectAPI (api, consumer, props, actions) {
  const { api: APIs, ...rest } = props;
  const { [api]: singleAPI, ...otherAPIs } = APIs;

  return merge(
    {},
    rest,
    {
      api: {
        [api]: new APIConnector(api, consumer, singleAPI, actions),
        ...otherAPIs,
      },
    },
  );
}


import { mapValues } from 'lodash';

export const types = {

};

export class APIConnector {

  constructor (state = {}, actions) {
    const { data: { schema } = {} } = state;

    this.models = mapValues(schema, (modelName, model) => (new Model(modelName, model)));
  }
}

class Model {

  constructor (modelName, model) {
    this.name = modelName;

    const { attributes, methods, relationships } = model;

  }

  create (args) {

  }

  filter () {

  }

  get () {

  }

}

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

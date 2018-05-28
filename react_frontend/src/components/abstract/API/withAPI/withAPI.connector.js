
import { mapValues } from 'lodash';
import { bindActionCreators } from 'redux';
import uuid from 'util/uuid';

import { APIFilteredSelector } from 'components/abstract/API';
import withAPIActionCreators from './withAPI.actions';

export const types = {

};

class Instance {

  constructor (model, data) {

  }

  fetch () {

  }

  save () {

  }

  delete () {

  }

}

class Model {

  constructor (api, modelName, modelSchema, modelData) {
    this.api = api;
    this.name = modelName;

    const { attributes, methods, relationships } = modelSchema;

    this.attributes = attributes;
    this.methods = methods;
    this.relationships = relationships;

    this.instances = mapValues(modelData, value => new Instance(this, value));
  }

  create (args) {

  }

  get () {

  }

  run (args) {

  }

  filter (fn) {

  }

}

export class APIConnector {

  constructor ({ name, sender, consumer, senders, models }) {
    this.name = name;
    this.senderName = sender;
    this.consumerName = consumer;
    this.senderNames = senders;
    this.modelNames = models;
  }

  select (state) {
    const api = APIFilteredSelector(
      this.name,
      this.senderName,
      this.consumerName,
      this.senderNames,
      this.modelNames,
    );
    const { status, authentication, senders, consumers, data } = api(state);
    this.status = status;
    this.authentication = authentication;
    this.senders = senders;
    this.consumers = consumers;
    this.data = data;

    this.isSender = this.senderName !== undefined;

    return {
      [this.name]: {
        status,
        authentication,
        senders,
        data,
      },
    };
  }

  connect (props) {
    const { api: { [this.name]: api, ...otherAPIs }, ...otherProps } = props;
    const { data: { schema, models } } = api;

    this.models = mapValues(
      schema,
      (modelSchema, modelName) => new Model(
        this,
        modelName,
        modelSchema,
        models[modelName],
      ),
    );

    return {
      api: {
        [this.name]: this,
        ...otherAPIs,
      },
      ...otherProps,
    };
  }

  register (props) {
    const { dispatch } = props;
    this.actions = bindActionCreators(withAPIActionCreators, dispatch);

    if (this.consumerName) {
      this.actions.onAPIConsumerRegister(this.name, this.consumerName, this.senderNames);
    }

    if (this.senderName) {
      this.actions.onAPISenderRegister(this.name, this.senderName);
    }
  }

  update () {
    const hasNewSenderValues = this.confirmNewSenderValues();

    if (hasNewSenderValues) {
      this.addConsumerReference();
      this.updateConsumerReference();
    }
  }

  confirmNewSenderValues () {
    let hasNewSenderValues = false;
    if (!this.isSender) {
      const { onAPIConsumerConfirmSenderValue } = this.actions;

      Object.entries(this.senders).forEach(([sender, { consumers = {} }]) => {
        if (!(this.consumerName in consumers)) {
          hasNewSenderValues = true;
          onAPIConsumerConfirmSenderValue(this.name, this.consumerName, sender);
        }
      });
    }

    return hasNewSenderValues;
  }

  addConsumerReference () {
    if (!this.isSender) {
      const { onAPIConsumerAddReference } = this.actions;

      const identifier = uuid();
      const query = this.constructConsumerQuery();

      onAPIConsumerAddReference(this.name, this.consumerName, identifier, query);
    }
  }

  setSenderValue (value) {
    if (this.isSender) {
      const { onAPISenderSetValue } = this.actions;

      onAPISenderSetValue(this.name, this.senderName, value);
    }
  }

  mergeConsumerValue (value) {
    if (!this.isSender) {
      this.consumerValue = {};
    }
  }

  constructConsumerQuery () {
    if (!this.isSender) {
      return {};
    }

    return null;
  }

}

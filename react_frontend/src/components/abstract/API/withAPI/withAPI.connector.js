
import { isEmpty, mapValues, merge } from 'lodash';
import { bindActionCreators } from 'redux';
import uuid from 'util/uuid';

import { APIFilteredSelector } from 'components/abstract/API';
import withAPIActionCreators from './withAPI.actions';

export const types = {

};

class Instance {

  constructor (model, data) {
    this.model = model;

    
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
    const { instances } = modelData;

    this.setAttributes(attributes);
    this.setMethods(methods);
    this.setRelationships(relationships);
    this.setInstances(instances);
  }

  setAttributes (attributes) {
    this.attributes = attributes;
  }

  setMethods (methods) {
    this.methods = methods;
  }

  setRelationships (relationships) {
    this.relationships = relationships;
  }

  setInstances (data) {
    // add validation from schema
    // pass attributes down
    this.instances = mapValues(data, value => new Instance(this, value));
  }

  create (args) {

  }

  get () {

  }

  run (args) {

  }

  filter (args) {
    return {
      [this.name]: {
        filter: {
          ...args,
        },
      },
    };
  }

}

export class APIConnector {

  constructor ({ name, sender, consumer, senders, models }) {
    this.name = name;
    this.senderName = sender;
    this.consumerName = consumer;
    this.senderNames = senders;
    this.modelNames = models;

    this.isSender = this.senderName !== undefined;
    this.isConsumer = this.consumerName !== undefined;
  }

  select (state) {
    const api = APIFilteredSelector(
      this.name,
      this.senderName,
      this.consumerName,
      this.senderNames,
      this.modelNames,
    );

    return { [this.name]: api(state) };
  }

  connect (props) {
    const { api: { [this.name]: api, ...otherAPIs }, ...otherProps } = props;
    const { data: { schema, models }, status, authentication, senders, consumers } = api;

    this.setModels(schema, models);
    this.setStatus(status);
    this.setAuthentication(authentication);
    this.setSenders(senders);
    this.setConsumer(consumers);
    this.setActiveConsumerResources();

    return {
      api: {
        [this.name]: this,
        ...otherAPIs,
      },
      ...otherProps,
    };
  }

  setModels (schema, models) {
    this.isReady = !isEmpty(schema);
    this.models = mapValues(
      schema,
      (modelSchema, modelName) => new Model(
        this,
        modelName,
        modelSchema,
        models[modelName] || {},
      ),
    );
  }

  setStatus (status) {
    this.status = status;
  }

  setAuthentication (authentication) {
    this.authentication = authentication;
  }

  setSenders (senders) {
    this.senders = senders;
  }

  setConsumer (consumers) {
    const { [this.consumerName]: consumer } = consumers;

    this.consumer = consumer;
  }

  setActiveConsumerResources () {
    if (this.isConsumer) {
      console.log(this);
    }
  }

  register (props) {
    const { dispatch } = props;
    this.actions = bindActionCreators(withAPIActionCreators, dispatch);

    if (this.isConsumer) {
      this.actions.onAPIConsumerRegister(this.name, this.consumerName, this.senderNames);
    }

    if (this.isSender) {
      this.actions.onAPISenderRegister(this.name, this.senderName);
    }
  }

  didUpdate () {
    const hasNewSenderValues = this.confirmNewSenderValues();

    if (hasNewSenderValues) {
      this.addConsumerReference();
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
    if (this.isConsumer) {
      const { onAPIConsumerAddReference } = this.actions;

      const identifier = uuid();
      this.query = this.constructConsumerQuery();

      if (this.query) {
        onAPIConsumerAddReference(this.name, this.consumerName, identifier, this.query);
      }
    }
  }

  setConsumerConverter (fn) {
    this.converter = fn;
  }

  constructConsumerQuery () {
    if (!this.isReady || !this.isConsumer) {
      return null;
    }

    const senderValues = mapValues(this.senders, ({ value }) => value);
    const queryArray = this.converter({ senders: senderValues, models: this.models });
    const query = queryArray.reduce((whole, part) => merge({}, whole, part));

    return query;
  }

  setSenderValue (value) {
    if (this.isSender) {
      const { onAPISenderSetValue } = this.actions;

      onAPISenderSetValue(this.name, this.senderName, value);
    }
  }

}

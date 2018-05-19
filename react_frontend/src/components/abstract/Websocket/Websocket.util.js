
export function encode (object) {
  return JSON.stringify(object);
}

export function decode (message) {
  return JSON.parse(message);
}

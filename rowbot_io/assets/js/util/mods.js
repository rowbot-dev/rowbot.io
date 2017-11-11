// extend trunc method for strings
String.prototype.trunc = function(n, useWordBoundary) {
  var isTooLong = this.length > n;
  var s_ = isTooLong ? this.substr(0,n-1) : this;
  var s_ = (useWordBoundary && isTooLong) ? s_.substr(0,s_.lastIndexOf(' ')) : s_;
  return  isTooLong ? s_ + '&hellip;' : s_;
}

// Trim string
if(!String.prototype.trim) {
  String.prototype.trim = function () {
    return this.replace(/^\s+|\s+$/g,'');
  }
}

String.prototype.contains = function (string) {
  return this.indexOf(string) !== -1;
}

String.prototype.score = function (query, exclusive) {
  var string = this;
  if (string === query) {
    return 1;
  }

  if (!query) {
    return exclusive ? 0 : 1;
  }

  var totalCharacterScore = 0;
  var queryLength = query.length;
  var stringLength = string.length;

  var indexInQuery = 0;
  var indexInString = 0;

  while (indexInQuery < queryLength) {
    let character = query[indexInQuery++];
    let lowerCaseIndex = string.indexOf(character.toLowerCase());
    let upperCaseIndex = string.indexOf(character.toUpperCase());
    let minIndex = Math.min(lowerCaseIndex, upperCaseIndex);
    if (minIndex === -1) {
      minIndex = Math.max(lowerCaseIndex, upperCaseIndex);
    }
    indexInString = minIndex;

    if (indexInString === -1) {
      return 0; // not found
    }

    // initial score
    let characterScore = 0.1;

    // same case bonus
    if (string[indexInString] === character) {
      characterScore += 0.1;
    }

    // start of string bonus
    if (indexInString === 0) {
      characterScore += 0.8;
    }

    string = string.substring(indexInString + 1, stringLength)

    totalCharacterScore += characterScore
  }

  var queryScore = totalCharacterScore / queryLength
  return ((queryScore * (queryLength / stringLength)) + queryScore) / 2
}

// Arrays
Array.prototype.contains = function (object) {
  return this.indexOf(object) !== -1;
}

Array.prototype.sum = function (object) {
  return this.reduce(function (f, s) {
    return f+s;
  });
}

Array.prototype.mean = function () {
  return this.sum() / this.length;
}

Array.prototype.index = function (property) {
  return this.reduce(function (whole, part) {
    whole[part[property]] = part;
    return whole;
  }, {});
}

Array.prototype.extend = function (array) {
  Array.prototype.push.apply(this, array);
}


Array.range = function (start, stop, step) {
  if (typeof stop == 'undefined') {
    // one param defined
    stop = start;
    start = 0;
  }

  if (typeof step == 'undefined') {
    step = 1;
  }

  if ((step > 0 && start >= stop) || (step < 0 && start <= stop)) {
    return [];
  }

  var result = [];
  for (var i = start; step > 0 ? i < stop : i > stop; i += step) {
    result.push(i);
  }

  return result;
};

if (!Array.prototype.last){
  Array.prototype.last = function(){
    return this[this.length - 1];
  };
};

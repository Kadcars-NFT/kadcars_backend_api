
var b64url = (function () {

  'use strict';

  var chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_=';

  function InvalidCharacterError(message) {
    this.message = message;
  }
  InvalidCharacterError.prototype = new Error();
  InvalidCharacterError.prototype.name = 'InvalidCharacterError';

  // encoder
  // [https://gist.github.com/999166] by [https://github.com/nignag]
  function base64UrlEncode(input) {
    var str = String(input);
    console.log(str)
    for (var block, charCode, idx = 0, map = chars, output = ''; str.charAt(idx | 0); output += map.charAt(63 & block >> 8 - idx % 1 * 8)) {
      charCode = str.charCodeAt(idx += 3 / 4);
      if (charCode > 0xFF) {
        throw new InvalidCharacterError("'btoa' failed: The string to be encoded contains characters outside of the Latin1 range.");
      }
      block = block << 8 | charCode;
    }
    return output;
  }

  // decoder
  // [https://gist.github.com/1020396] by [https://github.com/atk]
  function base64UrlDecode(input) {
    var str = (String(input)).replace(/[=]+$/, ''); // #31: ExtendScript bad parse of /=
    if (str.length % 4 === 1) {
      throw new InvalidCharacterError("'atob' failed: The string to be decoded is not correctly encoded.");
    }
    for (
      // initialize result and counters
      var bc = 0, bs, buffer, idx = 0, output = '';
      // get next character
      buffer = str.charAt(idx++); // eslint-disable-line no-cond-assign
      // character found in table? initialize bit storage and add its ascii value;
      ~buffer && (bs = bc % 4 ? bs * 64 + buffer : buffer,
        // and if not first of each 4 characters,
        // convert the first 8 bits to one ascii character
        bc++ % 4) ? output += String.fromCharCode(255 & bs >> (-2 * bc & 6)) : 0
    ) {
      // try to find character in table (0-63, not found => -1)
      buffer = chars.indexOf(buffer);
    }
    return output;
  }

  return { encode: base64UrlEncode, decode: base64UrlDecode };

})();

function strToUint8Array(s) {
  var i, b = new Uint8Array(s.length);
  for (i = 0; i < s.length; i++) b[i] = s.charCodeAt(i);
  return b;
}

function uint8ArrayToStr(a) {
  console.log(String.fromCharCode.apply(null, new Uint16Array(a)))
  return String.fromCharCode.apply(null, new Uint16Array(a));
}

function b64urlDecodeArr(input) {
  return strToUint8Array(b64url.decode(input));
}

function b64urlEncodeArr(input) {
  return b64url.encode(uint8ArrayToStr(input));
}

/**
 * Perform blake2b256 hashing.
 */
function hashBin(s) {
  return blake.blake2b(s, null, 32);
}

/**
 * Perform blake2b256 hashing, encoded as unescaped base64url.
 */
function hash(s) {
  return b64urlEncodeArr(hashBin(s));
}

function prepareCmdHash(msg) {
  var hshBin = hashBin(msg);
  var hsh = b64urlEncodeArr(hshBin);

  return [{hash: hsh, sig: undefined}];
}


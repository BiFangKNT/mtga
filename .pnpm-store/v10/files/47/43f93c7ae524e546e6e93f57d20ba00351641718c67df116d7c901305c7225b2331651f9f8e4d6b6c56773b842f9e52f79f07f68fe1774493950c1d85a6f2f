function createMock(name, overrides = {}) {
  const proxyFn = function () {
    /** noop */
  };
  proxyFn.prototype.name = name;
  const props = {};
  const proxy = new Proxy(proxyFn, {
    get(_target, prop) {
      if (prop === "caller") {
        return null;
      }
      if (prop === "__createMock__") {
        return createMock;
      }
      if (prop === "__mock__") {
        return true;
      }
      if (prop in overrides) {
        return overrides[prop];
      }
      if (prop === "then") {
        return (fn) => Promise.resolve(fn());
      }
      if (prop === "catch") {
        return (_fn) => Promise.resolve();
      }
      if (prop === "finally") {
        return (fn) => Promise.resolve(fn());
      }
      return (props[prop] =
        props[prop] || createMock(`${name}.${prop.toString()}`));
    },
    apply(_target, _this, _args) {
      return createMock(`${name}()`);
    },
    construct(_target, _args, _newT) {
      return createMock(`[${name}]`);
    },
    enumerate() {
      return [];
    },
  });
  return proxy;
}

export default createMock("mock");

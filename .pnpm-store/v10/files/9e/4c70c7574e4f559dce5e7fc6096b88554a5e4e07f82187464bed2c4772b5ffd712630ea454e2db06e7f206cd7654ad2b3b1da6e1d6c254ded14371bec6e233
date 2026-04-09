/* eslint-disable */

interface _MockFunction<F> {
  (...args: any[]): F;
  new (...args: any[]): F;
  readonly __mock__: true;
  readonly __createMock__: typeof createMock;
  then<T>(fn: () => T): Promise<T>;
  catch<T>(fn: () => T): Promise<void>;
  finally(fn: () => void): Promise<void>;
}

declare function createMock(
  name: string,
  overrides?: Record<string, any>,
): MockFunction;

type MockFunction = _MockFunction<MockFunction> & {
  readonly [key: string | symbol]: MockFunction;
};

declare const mock: MockFunction;

export default mock;

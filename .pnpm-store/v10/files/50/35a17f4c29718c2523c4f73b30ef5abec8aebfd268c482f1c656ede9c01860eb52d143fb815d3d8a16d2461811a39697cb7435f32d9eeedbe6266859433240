export interface ObjectFactory<T extends Function> {
    /**
     * The name of the factory function.
     * @example 'createUseFetch'
     */
    name: string;
    factory: T;
}
/**
 * Define a factory for a function that should be registered for automatic key injection.
 * @since 4.2.0
 * @param factory
 */
export declare function defineKeyedFunctionFactory<T extends Function>(factory: ObjectFactory<T>): T;

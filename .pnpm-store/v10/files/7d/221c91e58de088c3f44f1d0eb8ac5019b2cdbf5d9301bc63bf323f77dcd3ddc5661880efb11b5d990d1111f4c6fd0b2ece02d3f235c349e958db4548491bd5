//#region src/_url.d.ts
type URLInit = {
  protocol: string;
  host: string;
  pathname: string;
  search: string;
};
/**
* URL wrapper with fast paths to access to the following props:
*
*  - `url.pathname`
*  - `url.search`
*  - `url.searchParams`
*  - `url.protocol`
*
* **NOTES:**
*
* - It is assumed that the input URL is **already encoded** and formatted from an HTTP request and contains no hash.
* - Triggering the setters or getters on other props will deoptimize to full URL parsing.
* - Changes to `searchParams` will be discarded as we don't track them.
*/
declare const FastURL: {
  new (url: string | URLInit): URL & {
    _url: URL;
  };
};
//#endregion
export { FastURL as t };
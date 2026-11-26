export class SearchController {
  constructor(fetcher) {
    this.fetcher = fetcher;
    this.results = [];
    this.lastQuery = "";
  }

  async search(query) {
    this.lastQuery = query;
    const resp = await this.fetcher(query);
    // BUG 1: out-of-order response overwrites newer query results
    // BUG 2: API returns resp.items, not resp.results
    this.results = resp.results || [];
    return this.results;
  }
}

export function formatSearchResponse(items, query) {
  return {
    query,
    total: items.length,
    items,
  };
}

export function serializeFilters(state) {
  // BUG: ignores status and sort, loses filters on reload
  return state.q ? `?q=${encodeURIComponent(state.q)}` : "";
}

export function parseFilters(search) {
  // BUG: returns defaults instead of parsing URLSearchParams
  return { q: "", status: "all", sort: "newest" };
}

import test from "node:test";
import assert from "node:assert/strict";
import { SearchController } from "../web/src/searchController.js";
import { serializeFilters, parseFilters } from "../web/src/filterState.js";
import { renderComment } from "../web/src/commentRenderer.js";
import { formatSearchResponse } from "../api/server.js";

test("out-of-order search responses do not overwrite newer results", async () => {
  let resolveSlow;
  let resolveFast;
  const fetcher = (q) => {
    if (q === "a") return new Promise((r) => { resolveSlow = r; });
    return new Promise((r) => { resolveFast = r; });
  };
  const ctrl = new SearchController(fetcher);
  const p1 = ctrl.search("a");
  const p2 = ctrl.search("ab");
  resolveFast(formatSearchResponse([{ id: 2, title: "ab-match" }], "ab"));
  await p2;
  resolveSlow(formatSearchResponse([{ id: 1, title: "stale-a" }], "a"));
  await p1;
  assert.deepEqual(ctrl.results, [{ id: 2, title: "ab-match" }]);
});

test("filter state round-trips through URL query string", () => {
  const qs = serializeFilters({ q: "invoice #4", status: "open", sort: "oldest" });
  const parsed = parseFilters(qs);
  assert.deepEqual(parsed, { q: "invoice #4", status: "open", sort: "oldest" });
});

test("comment renderer escapes XSS payloads and blocks javascript: URLs", () => {
  const html = renderComment({
    author: '<img src=x onerror="alert(1)">',
    authorUrl: "javascript:alert(1)",
    body: '<script>steal()</script> & "hello"',
  });
  assert.ok(!html.includes("<script>"), "raw script tag leaked");
  assert.ok(!html.includes("<img"), "raw img tag leaked");
  assert.ok(!html.toLowerCase().includes("javascript:"), "javascript: URL leaked");
  assert.ok(html.includes("&lt;script&gt;"));
  assert.ok(html.includes("&amp;"));
});

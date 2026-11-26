import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import { applyCoupon, calculateTotal, nextModalFocus } from "../checkout.js";

const coupons = JSON.parse(fs.readFileSync(new URL("../data/coupons.json", import.meta.url), "utf8"));

test("lowercase and padded coupon codes work", () => {
  assert.equal(applyCoupon(100, " save10 ", coupons), 90);
  assert.equal(applyCoupon(100, "welcome20", coupons), 80);
});

test("tax-exempt items are not taxed", () => {
  const items = [
    { name: "Notebook", price: 50, qty: 1, taxExempt: false },
    { name: "Textbook", price: 50, qty: 1, taxExempt: true },
  ];
  // 10% coupon => taxable 45, exempt 45; 10% tax on taxable only = 4.50 => total 94.50
  assert.equal(calculateTotal(items, 0.10, "save10", coupons), 94.5);
});

test("modal focus wraps on Tab and Shift+Tab", () => {
  assert.equal(nextModalFocus(2, 3, false), 0);
  assert.equal(nextModalFocus(0, 3, true), 2);
  assert.equal(nextModalFocus(1, 3, false), 2);
});

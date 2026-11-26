export function applyCoupon(subtotal, code, coupons) {
  if (!code) return subtotal;
  // BUG: case-sensitive and no trim
  const rate = coupons[code] || 0;
  return Number((subtotal * (1 - rate)).toFixed(2));
}

export function calculateTotal(items, taxRate, couponCode, coupons) {
  const subtotal = items.reduce((s, it) => s + it.price * it.qty, 0);
  const discounted = applyCoupon(subtotal, couponCode, coupons);
  // BUG: taxes taxExempt items too
  const tax = Number((discounted * taxRate).toFixed(2));
  return Number((discounted + tax).toFixed(2));
}

export function nextModalFocus(currentIndex, total, shiftKey = false) {
  if (total <= 0) return -1;
  // BUG: clamps instead of wrapping
  if (shiftKey) return Math.max(0, currentIndex - 1);
  return Math.min(total - 1, currentIndex + 1);
}

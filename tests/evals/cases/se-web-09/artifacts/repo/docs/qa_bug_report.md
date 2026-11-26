# Checkout QA Bug Report
1. Coupon codes like `save10` fail because lookup is case-sensitive against `data/coupons.json`.
2. Tax-exempt items (`taxExempt: true`) are still being taxed in `calculateTotal`.
3. Keyboard focus helper `nextModalFocus(currentIndex, total, shiftKey)` gets stuck instead of wrapping from `0` to `total - 1` on Shift+Tab and `total - 1` to `0` on Tab.

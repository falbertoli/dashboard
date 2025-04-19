import {
  formatNumber,
  formatCurrency,
  formatArea,
  formatCompactNumber,
} from "../utils/formatters";

export default {
  install: (app) => {
    // Global properties
    app.config.globalProperties.$formatNumber = formatNumber;
    app.config.globalProperties.$formatCurrency = formatCurrency;
    app.config.globalProperties.$formatArea = formatArea;
    app.config.globalProperties.$formatCompactNumber = formatCompactNumber;

    // Optional: Add global directive
    app.directive("format-number", {
      mounted: (el, binding) => {
        const decimals = binding.arg || 2;
        el.innerHTML = formatNumber(el.innerHTML, decimals);
      },
      updated: (el, binding) => {
        const decimals = binding.arg || 2;
        el.innerHTML = formatNumber(el.innerHTML, decimals);
      },
    });
  },
};

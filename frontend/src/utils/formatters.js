// File: frontend/src/utils/initCustomFormatter.js

export function formatCurrency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
    useGrouping: true,
  }).format(value);
}

export function formatArea(sqft) {
  return (
    new Intl.NumberFormat("en-US", {
      style: "decimal",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
      useGrouping: true,
    }).format(sqft) + " ft²"
  );
}

// export function formatNumber(value, decimals = 2) {
//   if (value === null || value === undefined) return "N/A";
//   return new Intl.NumberFormat("en-US", {
//     minimumFractionDigits: decimals,
//     maximumFractionDigits: decimals,
//     useGrouping: true,
//   }).format(value);
// }

export function formatNumber(value, decimals = 0) {
  if (value === null || value === undefined) return "N/A";

  // Add logic to simplify large numbers if decimals == 'auto'
  if (decimals === "auto") {
    if (value >= 1_000_000_000) {
      return (value / 1_000_000_000).toFixed(1).replace(/\.0$/, "") + "B";
    } else if (value >= 1_000_000) {
      return (value / 1_000_000).toFixed(1).replace(/\.0$/, "") + "M";
    } else if (value >= 1_000) {
      return (value / 1_000).toFixed(1).replace(/\.0$/, "") + "K";
    }
  }

  return new Intl.NumberFormat("en-US", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
    useGrouping: true,
  }).format(value);
}

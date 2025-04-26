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
  const value =
    sqft >= 1_000_000
      ? (sqft / 1_000_000).toFixed(1) + "M"
      : sqft >= 1_000
      ? new Intl.NumberFormat("en-US").format(sqft)
      : sqft;

  return `${value} ft²`;
}

// export function formatArea(sqft) {
//   return (
//     new Intl.NumberFormat("en-US", {
//       style: "decimal",
//       minimumFractionDigits: 0,
//       maximumFractionDigits: 0,
//       useGrouping: true,
//     }).format(sqft) + " ft²"
//   );
// }

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
      return (value / 1_000_000_000).toFixed(0).replace(/\.0$/, "") + "B";
    } else if (value >= 1_000_000) {
      return (value / 1_000_000).toFixed(0).replace(/\.0$/, "") + "M";
    } else if (value >= 1_000) {
      return (value / 1_000).toFixed(0).replace(/\.0$/, "") + "K";
    }
  }

  return new Intl.NumberFormat("en-US", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
    useGrouping: true,
  }).format(value);
}

export function formatCompactNumber(value) {
  if (value === null || value === undefined) return "N/A";

  const absValue = Math.abs(value);
  let formatted;

  if (absValue >= 1_000_000_000) {
    formatted = (value / 1_000_000_000).toFixed(0) + "B";
  } else if (absValue >= 1_000_000) {
    formatted = (value / 1_000_000).toFixed(0) + "M";
  } else if (absValue >= 1_000) {
    formatted = (value / 1_000).toFixed(0) + "K";
  } else {
    formatted = value.toFixed(0).toString();
  }

  return formatted.replace(/\.0(?=[KMGB])/, ""); // strip trailing ".0" if unnecessary
}

export function formatTotal(value, forceUnit = null) {
  if (value === null || value === undefined) return "N/A";

  const absValue = Math.abs(value);
  let divisor = 1;
  let suffix = "";

  switch (forceUnit) {
    case "B":
      divisor = 1_000_000_000;
      suffix = "B";
      break;
    case "M":
      divisor = 1_000_000;
      suffix = "M";
      break;
    case "K":
      divisor = 1_000;
      suffix = "K";
      break;
    default:
      if (absValue >= 1_000_000_000) {
        divisor = 1_000_000_000;
        suffix = "B";
      } else if (absValue >= 1_000_000) {
        divisor = 1_000_000;
        suffix = "M";
      } else if (absValue >= 1_000) {
        divisor = 1_000;
        suffix = "K";
      }
  }

  const result = (value / divisor)
    .toFixed(0)
    .replace(/\.00$/, "")
    .replace(/(\.\d)0$/, "$1");
  return `${result}${suffix}`;
}

export function formatNumberDecimals(value, decimals = 2) {
  if (value === null || value === undefined) return "N/A";

  const absValue = Math.abs(value);
  let formatted;

  if (absValue >= 1_000_000_000) {
    formatted = (value / 1_000_000_000).toFixed(decimals) + "B";
  } else if (absValue >= 1_000_000) {
    formatted = (value / 1_000_000).toFixed(decimals) + "M";
  } else if (absValue >= 1_000) {
    formatted = (value / 1_000).toFixed(decimals) + "K";
  } else if (absValue == 0) {
    formatted = value.toFixed(0).toString();
  } else {
    formatted = value.toFixed(decimals).toString();
  }

  return formatted.replace(/\.0(?=[KMGB])/, "");
}

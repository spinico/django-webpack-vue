// SPDX-License-Identifier: MIT

import "./assets/styles/effects";

const isMobileWebKit = (): boolean => {
  const ua = navigator.userAgent;
  return /WebKit/.test(ua) && /Mobile/.test(ua);
};

// Add instances to the global namespace (defined in typings\custom.d.ts)
global.Mobile = isMobileWebKit();

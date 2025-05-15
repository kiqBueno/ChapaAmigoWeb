import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>
);

// Start of Tawk.to Script
const Tawk_API: { [key: string]: unknown } = {};
setTimeout(() => {
  (function () {
    Object.assign(Tawk_API, Tawk_API || {});
    const s1 = document.createElement("script"),
      s0 = document.getElementsByTagName("script")[0];
    s1.async = true;
    s1.src = "https://embed.tawk.to/63b7553d47425128790beaa6/1gm229upa";
    s1.charset = "UTF-8";
    s1.setAttribute("crossorigin", "*");
    if (s0.parentNode) {
      s0.parentNode.insertBefore(s1, s0);
    }
  })();
}, 3000); // Delay loading by 3 seconds
// End of Tawk.to Script

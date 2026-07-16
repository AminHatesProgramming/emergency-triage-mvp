// Compatibility entry point for the dependency-free Chrome DevTools Protocol check.
process.env.PWA_URL ||= "http://127.0.0.1:8765/";
require("./check_public_pwa_cdp.js");

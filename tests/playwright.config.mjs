import { defineConfig } from "@playwright/test";


export default defineConfig({
  testDir: ".",
  testMatch: "security_browser.spec.mjs",
  timeout: 30_000,
  use: {
    baseURL: "http://127.0.0.1:8877",
    headless: true,
  },
  webServer: {
    command: "python3 -m http.server 8877 --bind 127.0.0.1",
    cwd: "..",
    port: 8877,
    reuseExistingServer: false,
  },
});

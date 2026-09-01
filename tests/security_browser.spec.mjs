import { expect, test } from "@playwright/test";


test("assistant messages, artifacts, and data widgets preserve the browser trust boundary", async ({ page }) => {
  const pageErrors = [];
  const externalRequests = [];
  page.on("pageerror", (error) => pageErrors.push(String(error)));
  page.on("request", (request) => {
    if (request.url().startsWith("https://example.com/probe")) {
      externalRequests.push(request.url());
    }
  });

  await page.goto("/tests/security_browser.html");
  await page.evaluate(() => {
    window.chat = new customdhx.ChatWidget("#root", {
      persistence: false,
      enableArtifacts: true,
      messages: [{
        role: "assistant",
        content: [
          '<img src=x onerror="parent.__messageXss=1"> [unsafe](javascript:parent.__linkXss=1)',
          "",
          '::::artifact{title="Preview" type="text/html"}',
          '<script>try{parent.__artifactXss=1}catch(e){};fetch("https://example.com/probe").catch(()=>{});console.log("sandboxed")</script><p id="inside">safe preview</p>',
          "::::",
        ].join("\n"),
      }],
    });
  });

  const message = page.locator(".message-content").first();
  await expect(message).toContainText("<img");
  await expect(message.locator("img")).toHaveCount(0);
  await expect(message.locator("a")).toHaveAttribute("href", /#$/);
  expect(await page.evaluate(() => window.__messageXss)).toBeUndefined();

  await page.locator(".artifact-icon:not(.is-building)").click();
  const iframe = page.locator(".artifact-preview iframe");
  await expect(iframe).toHaveAttribute("sandbox", "allow-scripts");
  await expect(iframe.contentFrame().locator("#inside")).toHaveText("safe preview");
  expect(await page.evaluate(() => window.__artifactXss)).toBeUndefined();
  expect(externalRequests).toEqual([]);

  await page.evaluate(() => {
    window.cards = new customdhx.CardPanel("#cards", {cards: [{
      id: "one",
      title: "Safe",
      icon: '<img src=x onerror="parent.__cardIconXss=1">',
      contentHtml: '<strong>Allowed</strong><img src=x onerror="parent.__cardContentXss=1"><script>parent.__cardScriptXss=1</script>',
    }]});
    window.grid = new dhx.Grid("grid", {
      columns: [{id: "value", header: [{text: "Value"}], htmlEnable: true}],
      data: [{id: "one", value: '<img src=x onerror="parent.__gridXss=1"><strong>Grid</strong>'}],
    });
    window.list = new dhx.List("list", {
      htmlEnable: true,
      data: [{id: "one", value: '<img src=x onerror="parent.__listXss=1"><strong>List</strong>'}],
    });
  });

  await expect(page.locator(".card-card")).toBeVisible();
  await expect(page.locator(".card-content strong")).toHaveText("Allowed");
  await expect(page.locator(".card-icon")).toContainText("<img");
  await expect(page.locator("#grid strong")).toHaveText("Grid");
  await expect(page.locator("#list strong")).toHaveText("List");
  expect(await page.evaluate(() => Boolean(
    window.__cardIconXss
    || window.__cardContentXss
    || window.__cardScriptXss
    || window.__gridXss
    || window.__listXss
  ))).toBe(false);
  expect(pageErrors).toEqual([]);
});

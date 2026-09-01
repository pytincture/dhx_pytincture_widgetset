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

test("chat retention, fields, console data, and model context stay bounded", async ({ page }) => {
  await page.goto("/tests/security_browser.html");
  const result = await page.evaluate(async () => {
    localStorage.clear();
    sessionStorage.clear();
    window.boundedChat = new customdhx.ChatWidget("#root", {
      persistence: false,
      maxMessages: 3,
      maxMessageChars: 1000,
      includeArtifactConsoleInSend: false,
    });
    await window.boundedChat._readyPromise;
    for (let index = 0; index < 6; index += 1) {
      window.boundedChat.addMessage({
        role: "assistant",
        content: "x".repeat(2000),
        tools: Array.from({ length: 60 }, (_, toolIndex) => ({
          id: `tool-${toolIndex}`,
          output: "y".repeat(30000),
        })),
      });
    }
    const app = window.boundedChat._app;
    for (let artifactIndex = 0; artifactIndex < 25; artifactIndex += 1) {
      const id = `artifact-${artifactIndex}`;
      app._artifactConsoleOrder.push(id);
      app._artifactConsole.set(id, Array.from({ length: 150 }, () => ({
        level: "log",
        items: ["z".repeat(1000)],
      })));
    }
    let sendPayload = null;
    window.boundedChat.on("send", (payload) => {
      sendPayload = payload;
      return true;
    });
    app.els.queryInput.value = "question";
    app.handleSubmit();
    const messages = window.boundedChat.getMessages();
    const serializedConsole = app._serializeArtifactConsole();
    const contentStorageKey = app._storageKeys.chats;

    const persistedRoot = document.createElement("div");
    persistedRoot.id = "persisted-root";
    persistedRoot.style.cssText = "width:1000px;height:700px";
    document.body.appendChild(persistedRoot);
    window.persistedChat = new customdhx.ChatWidget("#persisted-root", {
      storageKey: "bounded-security-chat",
      persistence: "local",
      maxMessages: 100,
      maxStorageBytes: 16384,
    });
    await window.persistedChat._readyPromise;
    for (let index = 0; index < 40; index += 1) {
      window.persistedChat.addMessage({
        role: "assistant",
        content: `message-${index}-${"p".repeat(1000)}`,
        tools: [{ output: "secret-tool-output" }],
        meta: { secret: "secret-meta" },
      });
    }
    const persistedApp = window.persistedChat._app;
    const stored = localStorage.getItem(persistedApp._storageKeys.chats) || "";
    return {
      messageCount: messages.length,
      maxContent: Math.max(...messages.map((message) => message.content.length)),
      maxTools: Math.max(...messages.map((message) => message.tools.length)),
      consoleArtifacts: serializedConsole.length,
      maxConsoleEntries: Math.max(...serializedConsole.map((entry) => entry.entries.length)),
      consoleItemLength: serializedConsole[0].entries[0].items[0].length,
      consoleSent: Object.prototype.hasOwnProperty.call(sendPayload || {}, "artifactConsole"),
      disabledPersistenceStored: localStorage.getItem(contentStorageKey),
      storedBytes: new TextEncoder().encode(stored).length,
      storedContainsToolOrMeta: stored.includes("secret-tool-output") || stored.includes("secret-meta"),
    };
  });

  expect(result.messageCount).toBe(3);
  expect(result.maxContent).toBeLessThanOrEqual(1000);
  expect(result.maxTools).toBeLessThanOrEqual(50);
  expect(result.consoleArtifacts).toBeLessThanOrEqual(20);
  expect(result.maxConsoleEntries).toBeLessThanOrEqual(100);
  expect(result.consoleItemLength).toBeLessThanOrEqual(500);
  expect(result.consoleSent).toBe(false);
  expect(result.disabledPersistenceStored).toBeNull();
  expect(result.storedBytes).toBeLessThanOrEqual(16384);
  expect(result.storedContainsToolOrMeta).toBe(false);
});

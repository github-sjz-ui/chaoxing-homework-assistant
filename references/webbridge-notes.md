# WebBridge Notes for Chaoxing Homework Extraction

## Health Check

Always start with:

```powershell
~/.kimi-webbridge/bin/kimi-webbridge status
```

Required state: `running: true` and `extension_connected: true`.

If stuck:

```powershell
Remove-Item ~/.kimi-webbridge/daemon.pid -Force
~/.kimi-webbridge/bin/kimi-webbridge start
```

## Navigating Chaoxing

1. Start from the course URL provided by the user.
2. The homework list is loaded inside an iframe. Use `evaluate` to get the iframe `src`:

```javascript
const iframe = document.querySelector("iframe");
return iframe ? iframe.src : "no iframe";
```

3. Navigate to that iframe URL directly for the homework list.
4. Each homework item has an `onclick="goTask(this)"` with a `data` attribute containing the task URL. Extract those URLs and navigate to each.

## Fetching Raw HTML

Do not rely on `document.body.innerText` — it loses encoding. Use `fetch()` in the page context:

```javascript
(async () => {
  const resp = await fetch(location.href);
  const buf = await resp.arrayBuffer();
  const bytes = new Uint8Array(buf);
  let binary = '';
  for (let i = 0; i < bytes.byteLength; i++) binary += String.fromCharCode(bytes[i]);
  return btoa(binary);
})()
```

Decode the returned base64 as UTF-8.

## Common Pitfalls

- **Encoding**: Chaoxing pages are UTF-8. PowerShell console may display them as GBK, but files written in UTF-8 are correct.
- **Malformed HTML**: `<div class="questionLi">` blocks may not be closed properly. Use regex matching on `id="question\d+"` to split blocks.
- **Fill-in-the-blank answers**: Correct answers may not be present in the HTML; fill them in manually when found empty.
- **Sessions**: Use a dedicated session name (e.g., `chaoxing-homework`) to isolate tabs.

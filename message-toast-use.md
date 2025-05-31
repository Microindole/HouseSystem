
# message-toast.js 模块使用指南

`message-toast.js` 是一个用于在网页中显示美观、非阻塞式消息提示（Toasts）、警告框（Alerts）和确认框（Confirms）的 JavaScript 模块。它会自动在页面加载时初始化，并提供全局函数方便调用。

## 1. 引入模块

首先，确保在您的 HTML 文件中正确引入了 `message-toast.js` 脚本。通常，这会在 `<head>` 标签或者 `<body>` 标签的末尾完成：

```html
    <script src="{{ url_for('static', filename='js/common/message-toast.js') }}"></script>
```

模块初始化后，会在 `window` 对象上挂载以下几个便捷函数：
* `window.showMessage(message, type, duration)`
* `window.showAlert(message, options)`
* `window.showConfirm(message, options)`

以及一个 `MessageToast`类的实例：
* `window.messageToast` (包含 `success()`, `error()`, `warning()`, `info()`, `show()`, `alert()`, `confirm()`, `clear()` 等方法)

## 2. 显示浮动提示 (Toast)

浮动提示（Toast）是一种短暂的、非模态的通知，通常用于显示操作成功、警告或一般信息。

### 2.1 使用全局函数 `window.showMessage()`

这是最推荐的调用方式。

**参数:**

* `message` (String): 需要显示的消息内容。
* `type` (String, 可选): 消息的类型。默认为 `'success'`。
    * 有效类型包括:
        * `'success'` (成功)
        * `'error'` (错误)
        * `'warning'` (警告)
        * `'info'` (信息)
* `duration` (Number, 可选): 消息显示的持续时间（毫秒）。默认为 `3000` (3秒)。

**示例:**

```javascript
// 显示成功消息 (默认类型和时长)
if (window.showMessage) {
    window.showMessage("操作成功完成！");
} else {
    alert("操作成功完成！"); // Fallback
}

// 显示错误消息，持续5秒
if (window.showMessage) {
    window.showMessage("发生了一个错误，请重试。", "error", 5000);
} else {
    alert("发生了一个错误，请重试。"); // Fallback
}

// 显示警告消息
if (window.showMessage) {
    window.showMessage("请注意，您的输入有风险。", "warning");
} else {
    alert("请注意，您的输入有风险。"); // Fallback
}

// 显示一般信息
if (window.showMessage) {
    window.showMessage("系统将于今晚10点进行维护。", "info", 7000);
} else {
    alert("系统将于今晚10点进行维护。"); // Fallback
}
```

### 2.2 使用 `window.messageToast` 实例的便捷方法

模块还提供了一个 `window.messageToast` 实例，你可以通过它调用特定类型的方法：

* `window.messageToast.success(message, duration)`
* `window.messageToast.error(message, duration)`
* `window.messageToast.warning(message, duration)`
* `window.messageToast.info(message, duration)`

**示例:**

```javascript
if (window.messageToast) {
    window.messageToast.success("用户资料已更新。");
    window.messageToast.error("文件上传失败，请检查文件格式。", 4000);
    window.messageToast.warning("您的会话即将过期。");
    window.messageToast.info("欢迎回来！", 2000);
}
```

## 3. 显示警告框 (Alert)

警告框用于显示需要用户确认的重要信息，它会替代浏览器原生的 `alert()`，但提供更美观的样式和更好的用户体验。模块中的 `alert` 是基于 `confirm` 实现的，只有一个确认按钮。

### 使用全局函数 `window.showAlert()`

**参数:**

* `message` (String): 需要显示的警告信息。
* `options` (Object, 可选): 配置选项。
    * `title` (String, 可选): 警告框的标题。默认为 `'提示'`。
    * `buttonText` (String, 可选): 确认按钮的文本。默认为 `'确定'`。
    * `type` (String, 可选): 警告框的类型，影响图标和按钮颜色。默认为 `'info'`。
        * 有效类型: `'success'`, `'error'`, `'warning'`, `'info'`。

**返回值:**

* `Promise<void>`: 当用户点击确认按钮后，Promise 会 resolve。

**示例:**

```javascript
async function performAction() {
    // ... 一些操作 ...
    if (window.showAlert) {
        await window.showAlert("您的操作已成功提交。", { title: "操作结果", type: "success" });
        console.log("用户已确认成功提示");
    } else {
        alert("您的操作已成功提交。");
    }
}

async function handleError() {
    if (window.showAlert) {
        await window.showAlert("加载数据失败，请刷新页面重试。", { title: "加载错误", type: "error", buttonText: "知道了" });
    } else {
        alert("加载数据失败，请刷新页面重试。");
    }
}
```

## 4. 显示确认框 (Confirm)

确认框用于获取用户的肯定或否定选择，替代浏览器原生的 `confirm()`。

### 使用全局函数 `window.showConfirm()`

**参数:**

* `message` (String): 需要用户确认的消息。
* `options` (Object, 可选): 配置选项。
    * `title` (String, 可选): 确认框的标题。默认为 `'确认操作'`。
    * `confirmText` (String, 可选): "确定"按钮的文本。默认为 `'确定'`。
    * `cancelText` (String, 可选): "取消"按钮的文本。默认为 `'取消'`。如果设为 `null` 或空字符串，则不显示取消按钮（行为类似 Alert）。
    * `type` (String, 可选): 确认框的类型，影响图标和按钮颜色。默认为 `'warning'`。
        * 有效类型: `'success'`, `'error'`, `'warning'`, `'info'`。

**返回值:**

* `Promise<boolean>`:
    * 如果用户点击"确定"按钮，Promise resolve 为 `true`。
    * 如果用户点击"取消"按钮或关闭对话框，Promise resolve 为 `false`。

**示例:**

```javascript
async function deleteItem(itemId) {
    let confirmed = false;
    if (window.showConfirm) {
        confirmed = await window.showConfirm(`您确定要删除项目 ${itemId} 吗？此操作无法撤销。`, {
            title: "删除确认",
            confirmText: "是的，删除",
            cancelText: "不，保留",
            type: "warning" // 通常删除操作用 warning 或 error 类型
        });
    } else {
        confirmed = confirm(`您确定要删除项目 ${itemId} 吗？此操作无法撤销。`); // Fallback
    }

    if (confirmed) {
        console.log(`项目 ${itemId} 已被删除。`);
        // 在这里执行删除操作的逻辑...
        if (window.showMessage) {
            window.showMessage(`项目 ${itemId} 已成功删除。`, "success");
        }
    } else {
        console.log(`用户取消了删除项目 ${itemId} 的操作。`);
        if (window.showMessage) {
            window.showMessage("删除操作已取消。", "info");
        }
    }
}

// 调用示例
// deleteItem(123);
```

## 5. 清除所有当前显示的 Toast 消息

如果需要手动清除屏幕上所有当前正在显示的 Toast 消息，可以使用 `window.messageToast` 实例的 `clear()` 方法。

```javascript
if (window.messageToast) {
    window.messageToast.clear();
}
```
这对于在页面跳转或执行某些重置操作时非常有用。

## 6. 样式和自定义

模块的样式（如颜色、位置、大小）是在 JavaScript 文件内部通过 `style.cssText` 设置的。
* **Toast 消息容器 (`.toast-container`)**: 默认固定在右上角 (`top: 30px; right: 20px;`)。之前的版本中，`top` 可能是 `20px`。
* **Toast 消息本身 (`.message-toast`)**: 具有内边距、圆角、阴影等。
    * 之前的内边距可能是 `12px 20px`，字体大小 `14px`。当前版本中，可能已调整为 `padding: 15px 25px;` 和 `font-size: 15px;` 以使其稍大。
* **颜色**: 不同类型的消息（success, error, warning, info）使用不同的渐变背景色。

如果您需要更深度的自定义，可以直接修改 `message-toast.js` 文件中的相关样式代码，或者通过覆盖 CSS 类的方式（如果模块的 CSS 类名是稳定的且不被内联样式完全覆盖）。

---

通过以上方法，您可以方便地在您的项目中使用 `message-toast.js` 模块来增强用户界面的消息提示体验。

# 文档转换差异说明

## 整体情况

所有文档内容已完整转换，无显著内容遗漏。以下为已知的预期差异：

## 预期差异（不影响内容完整性）

1. **PlantUML 序列图** → ASCII 文本图
   - 文件：`auth/server-auth-guide.html`
   - 原文使用 PlantUML 渲染序列图，HTML 版本用 ASCII art 替代

2. **视频文件**
   - 文件：`auth/dynamic-client.html`、`auth/server-auth-guide.html`
   - 原文嵌入了 .mov 视频演示，HTML 版本中视频被省略（仅保留文字说明）

3. **删除线内容**
   - 文件：`auth/system-auth.html`
   - 原文中代码示例有删除线标记（表示废弃），HTML 版本保留代码但未加删除线样式

4. **颜色标注**
   - 原文部分文字使用红色/背景色标注重点，HTML 版本统一用 `<strong>` 或 `<code>` 替代

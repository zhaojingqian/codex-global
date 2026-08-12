---
name: mcp-server-center-docs
version: 0.1.2
description: Aone MCP 网关开发文档：开发/接入 MCP Server、鉴权（OAuth/Private Token/BUC SSO）、MCP-Lite 协议、发布调试、质量扫描。提到 Interface Transform/Zetta/x-zetta- 时不适用（走 Zetta 文档）。
x-source: aone-open
---

# Aone MCP 网关开发者文档

本 skill 包含 Aone MCP 网关的完整开发者文档，帮助开发者在 Aone MCP 平台上开发、调试、发布 MCP Server。

> **在线预览**：[文档首页](https://contextlab.alibaba-inc.com/skill/mcp-server-center-docs/latest/files/index.html)（ContextLab 托管，可直接在浏览器中查阅所有 HTML 文档）

## 适用范围

本文档**仅适用于 Aone MCP 网关**（即 Aone 开放平台上除 Interface Transform 以外的所有接入类型）。

**不覆盖以下内容：**

- **Zetta 网关**（即 Aone 开放平台上接入类型为「Interface Transform」的 MCP Server）
  - Zetta 网关将已有 HSF/HTTP 接口直接转化为 MCP Server，底层由 [ZettaGate](https://aigw-portal.alibaba-inc.com/) 提供服务
  - Zetta 网关文档请参考：[Welcome to ZettaGate](https://alidocs.dingtalk.com/i/nodes/gvNG4YZ7Jnxop15OCypkllMXW2LD0oRE)
  - Interface Transform 接入指南：[HSF / HTTP 接口转 MCP【ZETTA】](https://alidocs.dingtalk.com/i/nodes/N7dx2rn0JbxOaqnACy3mEoNdWMGjLRb3)

如果用户询问的是 Interface Transform 类型或 Zetta 网关相关问题（如 `x-zetta-` 前缀的 Header 透传、Zetta 的访问控制配置等），应引导用户查阅上述 Zetta 文档。

## 文档结构

按以下主题组织，根据用户问题定位到对应文档：

### 概览与使用
| 文档 | 路径 | 内容 |
|------|------|------|
| Aone MCP 介绍 | `overview/intro.html` | MCP 协议简介、Aone MCP 平台定位、整体架构 |
| 使用 MCP Server | `overview/usage.html` | 用户如何连接和使用 MCP Server（Cursor、Claude Code、Aone Copilot 等客户端配置） |

### 开发 MCP Server
| 文档 | 路径 | 内容 |
|------|------|------|
| 开发概览 | `develop/overview.html` | 接入方式选择（HTTP/HSF/Java SDK/OpenAPI/代理/沙箱） |
| Java 研发手册 | `develop/java-handbook.html` | Java SDK 接入详细步骤 |
| 版本更新记录 | `develop/java-sdk-changelog.html` | mcp-lite-hsf-server-starter 各版本功能变更 |
| FaaS 研发手册 | `develop/faas-handbook.html` | Node.js FaaS 应用接入 |
| Python 研发手册 | `develop/python-handbook.html` | Python FaaS 应用接入 |
| MCP 网关 HTTP 接入规范 | `develop/gateway-http-spec.html` | MCP-Lite 协议详细规范（tools/list、tools/call 接口定义） |
| OpenAPI 转为 MCP | `develop/openapi-transform.html` | 已有 OAS/Swagger 文档转 MCP |
| 代理已有 MCP Server | `develop/proxy-existing.html` | 代理已部署的 MCP Server |
| 在沙箱中运行 command | `develop/sandbox-command.html` | 命令行工具托管 |
| 沙箱调试与运维 | `develop/sandbox-debug.html` | 沙箱环境调试 |
| 编排工具集 | `develop/compose-tools.html` | 组合已有市场工具为新 MCP Server |
| Java 客户端连接参考 | `develop/java-client-reference.html` | Java 代码连接 MCP Server 示例 |
| 单应用多 MCP Server | `develop/multi-server.html` | 一个应用注册多个独立 MCP Server |
| HSF 多套环境适配 | `develop/hsf-multi-env.html` | HSF 多环境部署方案 |
| Annotations & Output Schema | `develop/annotations-output-schema.html` | 工具注解和输出 Schema 定义 |

### 研发流程与调试
| 文档 | 路径 | 内容 |
|------|------|------|
| MCP 发布流程 | `develop/publish-flow.html` | 从开发到上线的完整发布流程 |
| 质量扫描 | `develop/quality-scan.html` | MCP 工具质量检测 |
| 调用链路查看 | `develop/call-trace.html` | 查看工具调用链路与节点数据 |
| 日常环境调试代理 | `develop/debug-proxy.html` | 日常环境的调试代理配置 |

### 进阶配置
| 文档 | 路径 | 内容 |
|------|------|------|
| Server 选项调整 | `develop/server-options.html` | MCP Server 的可选配置项 |
| HTTP 请求头配置 | `develop/http-headers-config.html` | 自定义请求头透传配置 |
| 网关默认下发请求头 | `develop/gateway-default-headers.html` | 网关自动附加的请求头说明 |
| 鉴权开发指南 | `develop/best-practices.html` | MCP Server 中的鉴权最佳实践 |

### 认证与授权
| 文档 | 路径 | 内容 |
|------|------|------|
| 身份认证概览 | `auth/auth-overview.html` | 凭证类型总览（Private Token、OAuth、应用可信身份） |
| 静态客户端接入 | `auth/static-client.html` | 静态 OAuth 客户端注册与接入 |
| Client 注册流程 | `auth/client-registration.html` | MCP Client 注册步骤 |
| OAuth 授权扩展 | `auth/oauth-extensions.html` | OAuth 扩展字段说明 |
| 动态客户端使用 | `auth/dynamic-client.html` | 动态客户端注册与使用 |
| 系统间授权 | `auth/system-auth.html` | 应用间（M2M）授权方案 |
| Server 鉴权接入指南 | `auth/server-auth-guide.html` | MCP Server 端如何验证用户身份 |
| BUC 应用免登 | `auth/buc-sso.html` | BUC SSO 免登集成方案 |

### 公告
| 文档 | 路径 | 内容 |
|------|------|------|
| 解除 60 秒超时限制 | `announcements/timeout-60s.html` | 长耗时工具调用配置 |
| 部门校验 | `announcements/2025-09-dept-check.html` | 2025-09 启用部门校验 |
| 域名校验 | `announcements/2025-08-domain-check.html` | 2025-08 MCP Server 域名校验 |
| Streamable HTTP | `announcements/2025-07-streamable-http.html` | 2025-07 Streamable HTTP Transport 支持 |

## 使用指引

回答用户问题时，按以下顺序处理：

1. 根据问题关键词定位到上述表格中的对应文档
2. 使用 Read 工具读取对应的 HTML 文件内容
3. 基于文档内容回答用户问题，给出具体的配置示例或代码片段

### 常见问题路由

- "怎么开发/接入 MCP Server" → 先读 `develop/overview.html` 确定接入方式，再读对应手册
- "MCP 鉴权/认证/token" → 读 `auth/auth-overview.html`，再按具体场景深入
- "MCP-Lite 协议/HTTP 规范" → 读 `develop/gateway-http-spec.html`
- "发布/上线" → 读 `develop/publish-flow.html`
- "调试/排查" → 读 `develop/call-trace.html` 或 `develop/debug-proxy.html`
- "请求头/header" → 读 `develop/gateway-default-headers.html` 和 `develop/http-headers-config.html`
- "OAuth/客户端注册" → 读 `auth/static-client.html` 或 `auth/dynamic-client.html`
- "超时/timeout" → 读 `announcements/timeout-60s.html`

## 核心概念速查

- **Aone MCP 网关**：集团统一 MCP 协议网关，将后端 HTTP/HSF 服务转换为标准 MCP 协议
- **MCP-Lite**：简化版 MCP 接入协议，开发者提供普通 HTTP 接口即可接入网关
- **MCP Provider**：开发者提供的后端 HTTP 服务，实现 `tools/list` 和 `tools/call` 接口
- **Private Token**：代码平台颁发的个人凭证，最简单的鉴权方式
- **MCP OAuth**：标准 OAuth2 授权流程，适用于 Agent 和需要用户授权的场景
- **应用可信身份**：系统间（M2M）调用的授权方式
- **BUC SSO**：阿里 BUC 统一登录体系的免登集成

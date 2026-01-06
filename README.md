🍌 NanoBanana API – ComfyUI 文生图 / 图生图节点

一个基于 NanoBanana / Gemini Image API 的 ComfyUI 自定义节点，
支持 文生图（Text to Image） 与 图生图（Image to Image，多参考图）。

✅ 纯 API 调用
✅ 不依赖本地模型
✅ 支持多张参考图
✅ 节点本身完全免费、开源

✨ 功能特性

📝 文生图（Text → Image）

🖼️ 图生图（Image → Image）

支持最多 5 张参考图

🔁 自动重试 empty_response

📐 支持多种 分辨率 / 宽高比

⚙️ 参数全部可在 ComfyUI 面板中配置

🔌 API 平台 / 模型 可扩展、可替换

📦 安装方式
方法一：手动安装（推荐）

进入你的 ComfyUI 目录：

ComfyUI/custom_nodes/


克隆本仓库：

git clone https://github.com/你的用户名/comfyui-nanobanana-api.git


重启 ComfyUI

方法二：ComfyUI Manager（如果你已提交）

在 ComfyUI Manager 中搜索：

NanoBanana

🧩 节点名称

在 ComfyUI 中显示为：

NanoBanana API (Text2Image / Image2Image)


分类位置：

NanoBanana

🖼️ 使用示例
文生图（Text → Image）

不连接任何 image_* 输入

填写 prompt

运行节点即可生成图片

图生图（Image → Image）

使用 Load Image 节点加载图片

将图片连接到：

image_1（主参考）

可选：image_2 ~ image_5

在 prompt 中描述你希望生成的内容

运行节点
<img width="2029" height="1509" alt="workflow" src="https://github.com/user-attachments/assets/d3f52964-14d1-4a76-b051-48cc444246b3" />

⚙️ 参数说明（逐项）
🔑 必填参数
api_key（STRING）

第三方 API Key

本项目不提供 API Key

示例：

sk-xxxxxxxxxxxxxxxxxxxx

prompt（STRING）

文本提示词

支持中文 / 英文

图生图时建议描述：

你希望在参考图基础上生成什么

🖼️ 可选图像输入
image_1 ~ image_5（IMAGE）

参考图片（可选）

至少连接一张即进入 图生图模式

不连接任何图片即为 文生图

📐 图像参数
image_size
选项	说明
512	小尺寸
1K	默认
2K	高分辨率
aspect_ratio
选项	比例
1:1	正方形
4:3	横向
16:9	横屏（默认）
9:16	竖屏
🎛️ 生成控制参数
temperature（FLOAT）

控制生成随机性

范围：0.1 ~ 1.5

建议：

0.5 ~ 0.8：稳定

1.0+：更发散、更创意

max_retry（INT）

当 API 返回 empty_response 时的重试次数

默认：3

最大：5

📤 输出
image（IMAGE）

ComfyUI 标准 IMAGE 输出

可直接连接：

Save Image

后处理节点

其他工作流

🔌 API 平台说明（重要）

本节点通过 第三方 API 平台 调用远程模型。

已验证可用的平台示例
https://www.geeknow.top/console

⚠️ 重要声明

本节点 完全免费、开源

本项目 不提供 API Key

本项目 不收取任何费用

本项目 不进行任何平台推广或广告

第三方平台的：

收费策略

套餐价格

使用限制

均与本项目作者无关。

使用前请自行阅读对应平台的服务条款。

🧠 技术实现说明（简要）

使用 Gemini Image generateContent 接口

ComfyUI IMAGE (torch.Tensor) ⇄ PIL.Image 自动转换

支持多图 inlineData 输入

自动处理：

Base64 编码

empty_response 重试

❓ 常见问题
Q：为什么不用本地模型？

A：这是一个 API 节点，目标是零显存、快速接入。

Q：图生图和文生图逻辑一样吗？

A：是的，仅区别在于：

是否向 API 发送 inlineData 图片

Q：会不会泄露 API Key？

A：不会，API Key 只在本地使用，不会被保存或上传。

📜 License

MIT License
自由使用、修改、分发
请保留原作者署名

❤️ 致谢

ComfyUI 社区

Gemini / NanoBanana API

所有测试与反馈的用户

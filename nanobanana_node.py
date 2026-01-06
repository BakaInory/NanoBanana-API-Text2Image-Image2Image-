import torch
import http.client
import json
import base64
import time
import numpy as np
from PIL import Image
import io

# ======================
# 工具函数
# ======================

def image_to_base64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def base64_to_image(data: str) -> Image.Image:
    return Image.open(io.BytesIO(base64.b64decode(data))).convert("RGB")


def pil_to_comfy(img: Image.Image):
    arr = np.array(img, copy=True).astype(np.float32) / 255.0
    tensor = torch.from_numpy(arr)[None,]  # shape: [1, H, W, C]
    return tensor



# ======================
# ComfyUI Node
# ======================

class NanoBananaGenerate:
    """
    NanoBanana API - Gemini Image
    支持 文生图 / 图生图（多参考）
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False}),
                "prompt": ("STRING", {"multiline": True}),
            },
            "optional": {
                "image_1": ("IMAGE",),
                "image_2": ("IMAGE",),
                "image_3": ("IMAGE",),
                "image_4": ("IMAGE",),
                "image_5": ("IMAGE",),
                "image_size": (["512", "1K", "2K"], {"default": "1K"}),
                "aspect_ratio": (["1:1", "4:3", "16:9", "9:16"], {"default": "16:9"}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.1, "max": 1.5}),
                "max_retry": ("INT", {"default": 3, "min": 1, "max": 5}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "generate"
    CATEGORY = "NanoBanana"

    # ======================
    # 主逻辑
    # ======================

    def generate(
        self,
        api_key,
        prompt,
        image_size="1K",
        aspect_ratio="16:9",
        temperature=0.7,
        max_retry=3,
        image_1=None,
        image_2=None,
        image_3=None,
        image_4=None,
        image_5=None,
    ):

        HOST = "geek.closeai.icu"
        MODEL = "gemini-2.5-flash-image-preview"
        PATH = f"/v1beta/models/{MODEL}:generateContent"

        # ===== 构建 parts =====
        parts = [{"text": prompt}]

        for img in [image_1, image_2, image_3, image_4, image_5]:
            if img is not None:
                 # ComfyUI IMAGE (torch.Tensor) → PIL
                img0 = img[0]
                if isinstance(img0, torch.Tensor):
                    img0 = img0.detach().cpu()
                    img0 = img0.clamp(0, 1).mul(255).to(torch.uint8).numpy()
                    pil = Image.fromarray(img0)

                parts.append({
                    "inlineData": {
                        "mimeType": "image/png",
                        "data": image_to_base64(pil)
                    }
                })

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": parts
                }
            ],
            "generationConfig": {
                "responseModalities": ["IMAGE"],
                "temperature": temperature,
                "topP": 0.9,
                "imageConfig": {
                    "imageSize": image_size,
                    "aspectRatio": aspect_ratio
                }
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # ===== 重试逻辑 =====
        for attempt in range(1, max_retry + 1):
            conn = http.client.HTTPSConnection(HOST, timeout=90)
            conn.request("POST", PATH, body=json.dumps(payload), headers=headers)
            res = conn.getresponse()
            raw = res.read().decode("utf-8")

            try:
                resp = json.loads(raw)
            except Exception:
                raise RuntimeError("NanoBanana 返回非 JSON")

            # 成功
            if res.status == 200 and "candidates" in resp:
                for part in resp["candidates"][0]["content"]["parts"]:
                    if "inlineData" in part:
                        img = base64_to_image(part["inlineData"]["data"])
                        return (pil_to_comfy(img),)

            # empty_response → 重试
            if "error" in resp and resp["error"].get("type") == "empty_response":
                time.sleep(1.2)
                continue

            raise RuntimeError(f"NanoBanana API Error: {resp}")

        raise RuntimeError("NanoBanana API: 多次重试仍 empty_response")

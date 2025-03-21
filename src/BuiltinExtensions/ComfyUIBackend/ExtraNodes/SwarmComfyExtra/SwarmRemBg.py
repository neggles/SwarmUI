from PIL import Image
import numpy as np
import torch

class SwarmRemBg:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
            }
        }

    CATEGORY = "SwarmUI/images"
    RETURN_TYPES = ("IMAGE", "MASK",)
    FUNCTION = "rem"

    def rem(self, images):
        from rembg import remove

        output = []
        masks = []
        for image in images:
            i = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            img = img.convert("RGBA")
            img = remove(img, post_process_mask=True)
            output.append(np.array(img).astype(np.float32) / 255.0)
            if 'A' in img.getbands():
                mask = np.array(img.getchannel('A')).astype(np.float32) / 255.0
                masks.append(1. - mask)
            else:
                masks.append(np.zeros((64,64), dtype=np.float32))
        return (torch.from_numpy(np.array(output)), torch.from_numpy(np.array(masks)))

NODE_CLASS_MAPPINGS = {
    "SwarmRemBg": SwarmRemBg,
}

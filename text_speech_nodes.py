import re
from typing import List, Tuple

class TextSpeechSplitNode:
    """拆分节点（无问题，保留）"""
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("非说话内容", "说话内容1", "说话内容2", "说话内容3", "说话内容4")
    FUNCTION = "split_speech_content"
    CATEGORY = "自定义节点/文本处理"
    TITLE = "文本说话内容拆分（稳定版）"

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"输入文本": ("STRING", {"multiline": True, "default": ""})}}

    def split_speech_content(self, 输入文本: str) -> Tuple[str, str, str, str, str]:
        pattern = r"([^\u4e00-\u9fa5]*(说|说道)[^\u4e00-\u9fa5]*：)[“]([\s\S]*?)[”]"
        matches = re.findall(pattern, 输入文本, flags=re.DOTALL)
        
        speech_contents = []
        non_speech_text = 输入文本
        for prefix, _, content in matches:
            speech_contents.append(content.strip())
            non_speech_text = non_speech_text.replace(f"{prefix}“{content}”", prefix[:-1])
        
        while len(speech_contents) < 4:
            speech_contents.append("")
        
        return (non_speech_text, speech_contents[0], speech_contents[1], speech_contents[2], speech_contents[3])

class TextSpeechMergeNode:
    """合并节点（重写为“分割-替换-拼接”逻辑，零错位）"""
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("合并后文本",)
    FUNCTION = "merge_speech_content"
    CATEGORY = "自定义节点/文本处理"
    TITLE = "英文文本说话内容合并（零错位版）"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "英文基础文本": ("STRING", {"multiline": True, "default": ""}),
                "说话内容1": ("STRING", {"default": ""}),
                "说话内容2": ("STRING", {"default": ""}),
                "说话内容3": ("STRING", {"default": ""}),
                "说话内容4": ("STRING", {"default": ""}),
                "匹配关键词": ("STRING", {"default": "said,says,whispered,whispering,spoke"}),
            },
        }

    def merge_speech_content(self, 英文基础文本: str, 说话内容1: str, 说话内容2: str, 说话内容3: str, 说话内容4: str, 匹配关键词: str) -> Tuple[str]:
        # 1. 预处理：整理关键词和说话内容（动态，无固定值）
        keywords = [k.strip().lower() for k in 匹配关键词.split(",") if k.strip()]
        if not keywords:
            keywords = ["said", "says", "whispered", "whispering", "spoke"]
        speech_list = [s.strip() for s in [说话内容1, 说话内容2, 说话内容3, 说话内容4] if s.strip()]
        if not speech_list:
            return (英文基础文本,)
        
        # 2. 核心逻辑：暴力匹配所有关键词（不区分大小写，无视后缀）
        # 生成匹配所有关键词的正则（不限制边界，只匹配关键词本身）
        pattern = re.compile(r"(" + "|".join(keywords) + r")", re.IGNORECASE)
        
        # 3. 分割文本为“非关键词段 + 关键词段”的列表
        parts = pattern.split(英文基础文本)
        final_parts = []
        speech_idx = 0  # 说话内容的索引
        
        # 4. 逐个拼接，遇到关键词就插入说话内容
        for part in parts:
            if part.lower() in keywords and speech_idx < len(speech_list):
                # 匹配到关键词，插入说话内容
                final_parts.append(f"{part}：“{speech_list[speech_idx]}”")
                speech_idx += 1
            else:
                # 非关键词段，直接保留
                final_parts.append(part)
        
        # 5. 拼接最终文本
        final_text = "".join(final_parts)
        return (final_text,)

# 节点注册
NODE_CLASS_MAPPINGS = {
    "TextSpeechSplitNode": TextSpeechSplitNode,
    "TextSpeechMergeNode": TextSpeechMergeNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextSpeechSplitNode": "文本说话内容拆分（稳定版）",
    "TextSpeechMergeNode": "英文文本说话内容合并（零错位版）"
}

if __name__ == "__main__":
    pass

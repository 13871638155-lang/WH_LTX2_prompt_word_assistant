from .text_speech_nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# 把节点映射暴露给ComfyUI（这一步是关键，确保ComfyUI能找到节点）
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

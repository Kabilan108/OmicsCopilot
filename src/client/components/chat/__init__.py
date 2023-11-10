# src/client/components/chat/__init__.py

import streamlit.components.v1 as components

import os


_DEBUG = True

if _DEBUG:
    _chat = components.declare_component(
        "chat",
        url="http://localhost:3001",
    )
else:
    _parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(_parent_dir, "frontend/build")
    _chat = components.declare_component("visx", path=build_dir)


def chat():
    return _chat()

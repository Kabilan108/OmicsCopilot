# app/components/charts/__init__.py

import os
import streamlit.components.v1 as _components


_RELEASE = False

if _RELEASE:
    _parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(_parent_dir, "frontend/build")
    _visx = _components.declare_component("visx", path=build_dir)
else:
    _visx = _components.declare_component(
        "visx",
        url="http://localhost:3001",
    )


def st_visx(data, opts, key=None):
    return _visx(data=data, opts=opts, default=[], key=key)


def volcano_plot(data, opts, key=None):
    return _visx(data=data, opts=opts, default=[], key=key)

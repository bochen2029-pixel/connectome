#!/usr/bin/env python
"""Inject scene.json into template.html -> scene.html (the artifact page)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "scene.json")
dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "scene.html")
data = open(src, encoding="utf-8").read()
json.loads(data)  # must be valid JSON before it goes into the page
# a "</script>" inside a snippet would end the data block early; escape the sequence inside the JSON
data = data.replace("</", "<\\/")
tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
assert tpl.count("/*__SCENE_JSON__*/") == 1
out = tpl.replace("/*__SCENE_JSON__*/", data)
open(dst, "w", encoding="utf-8").write(out)
print("wrote", dst, "%.2f MB" % (os.path.getsize(dst) / 1e6))

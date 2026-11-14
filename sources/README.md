# Sources

Scripts and data that build the PDFs and pages in this repo. Paths inside the scripts point to the build folder they were written in; adjust them before re-running.

- `kb/`: Knowledge Base topics (`t_*.py`), page template and builders (`build.py` makes the web page, `print.py` the PDF version)
- `guide/`: the Placement Guide (`build.py`, `process.py`, `style.css`) and the topic linker
- `final/`: makes the three PDFs with indexes, back-links, bookmarks and page numbers (`make.py`, `render.js`, `start.py`)
- `playbook/`: re-dating (`repace.py`), route chart (`route.py`) and Path A (`patha_pb.py`), applied in that order to `playbook.v23.html`
- `roadmap/`: Path A for the roadmap (`patha_roadmap.py`), applied to `placement-roadmap.v9.html`

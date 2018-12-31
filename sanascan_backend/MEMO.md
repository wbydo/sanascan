# git clone 後にやること
- `pipenv run sphinx-quickstart`を実行
- `Pipfile`の`apidoc`コマンド内をパッケージパスにする
- `conf.py`の編集
    - 秘伝のタレを記述
    - パスを変更


# conf.pyの秘伝のタレ

```python
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx'
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
]

html_theme = 'sphinx_rtd_theme'

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

intersphinx_mapping = {'python':('https://docs.python.org/ja/3.6/', None)}
```

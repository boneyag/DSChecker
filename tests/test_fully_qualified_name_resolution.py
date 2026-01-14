from dschecker_agent.llm_function_utils import get_fully_qualified_name
import os


code_path = os.path.join(os.path.dirname(__file__), "../src/data/code_snippets")

def test_fqn_resolution_for_simple_import():
    code = "from sklearn.compose import ColumnTransformer\ntransformer = ColumnTransformer()\ntransformed = transformer.fit_transform()"
    fqn = get_fully_qualified_name("ColumnTransformer", code)
    assert fqn == "sklearn.compose.ColumnTransformer"

    code = "from sklearn.cluster import DBSCAN\nclustering = DBSCAN().fit()"
    fqn = get_fully_qualified_name("DBSCAN", code)
    assert fqn == "sklearn.cluster.DBSCAN"


def test_fqn_resolution_for_member():
    code = "from sklearn.compose import ColumnTransformer\ntransformer = ColumnTransformer()\ntransformed = transformer.fit_transform()"
    fqn = get_fully_qualified_name("fit_transform", code)
    assert fqn == "sklearn.compose.ColumnTransformer.fit_transform"

    code = "from sklearn.cluster import DBSCAN\nclustering = DBSCAN().fit()"
    fqn = get_fully_qualified_name("fit", code)
    assert fqn == "sklearn.cluster.DBSCAN.fit"

    code = "import matplotlib.pyplot as plt\nfig, ax = plt.subplots()\nax.legend()"
    fqn = get_fully_qualified_name("legend", code)
    assert fqn == "matplotlib.axes.Axes.legend"


def test_fqn_resolution_for_expr():
    code = "import matplotlib.pyplot as plt\nplt.plot([1, 2])"
    fqn = get_fully_qualified_name("plot", code)
    assert fqn == "matplotlib.pyplot.plot"


def test_fqn_resolution_for_multiple_attr():
    code = "import os\nscript_dir = os.path.dirname(os.path.abspath(__file__))"
    fqn = get_fully_qualified_name("dirname", code)
    assert fqn == "os.path.dirname"

    fqn = get_fully_qualified_name("abspath", code)
    assert fqn == "os.path.abspath"


def test_fqn_code_snippet_6():
    with open(os.path.join(code_path, "6_matplotlib_setxticklabels.py")) as cf:
        code = cf.read()

    fqn = get_fully_qualified_name("read_csv", code)
    assert fqn == "pandas.read_csv"

    fqn = get_fully_qualified_name("set_major_locator", code)
    assert fqn == "matplotlib.axis.Axis.set_major_locator"

    fqn = get_fully_qualified_name("set_xticklabels", code)
    assert fqn == "matplotlib.axes.Axes.set_xticklabels"

    fqn = get_fully_qualified_name("unique", code)
    assert fqn == "pandas.unique"


def test_fqn_code_snippet_10():
    with open(os.path.join(code_path, "10_seaborn_lmplot.py")) as cf:
        code = cf.read()

    fqn = get_fully_qualified_name("lmplot", code)
    assert fqn == "seaborn.lmplot"

    fqn = get_fully_qualified_name("FacetGrid", code)
    assert fqn == "seaborn.FacetGrid"

    fqn = get_fully_qualified_name("map", code)
    assert fqn == "seaborn.FacetGrid.map"


def test_fqn_code_snippet_23c():
    with open(os.path.join(code_path, "23c_seaborn_heatmap.py")) as cf:
        code = cf.read()

    fqn = get_fully_qualified_name("drop", code)
    assert fqn == "pandas.DataFrame.drop"

    fqn = get_fully_qualified_name("pivot_table", code)
    assert fqn == "pandas.DataFrame.pivot_table"


def test_fqn_code_snippet_24c():
    with open(os.path.join(code_path, "24c_pandas_resetindex.py")) as cf:
        code = cf.read()

    fqn = get_fully_qualified_name("groupby", code)
    assert fqn == "pandas.DataFrame.groupby"

    fqn = get_fully_qualified_name("apply", code)
    assert fqn == "pandas.DataFrame.apply"

    fqn = get_fully_qualified_name("shift", code)
    assert fqn == "pandas.Series.shift"

    fqn = get_fully_qualified_name("reset_index", code)
    assert fqn == "pandas.DataFrame.reset_index"


def test_fqn_code_snippet_28():
    with open(os.path.join(code_path, "28_scikitlearn_predict.py")) as cf:
        code = cf.read()

    fqn = get_fully_qualified_name("fit", code)
    assert fqn == "sklearn.model_selection.GridSearchCV.fit"

    fqn = get_fully_qualified_name("predict", code)
    assert fqn == "sklearn.model_selection.GridSearchCV.best_estimator_.predict"


def test_fqn_code_snippet_30c():
    with open(os.path.join(code_path, "30c_matplotlib_text.py")) as cf:
        code = cf.read()

    fqn = get_fully_qualified_name("text", code)
    assert fqn == "matplotlib.pyplot.text"

    fqn = get_fully_qualified_name("strptime", code)
    assert fqn == "datetime.datetime.strptime"


def test_fqn_code_snippet_31():
    with open(os.path.join(code_path, "31_matplotlib_axvspan.py")) as cf:
        code = cf.read()

    fqn = get_fully_qualified_name("axvspan", code)
    assert fqn == "matplotlib.axes.Axes.axvspan"


def test_fqn_code_snippet_33():
    with open(os.path.join(code_path, "33_scikitlearn_pipeline.py")) as cf:
        code = cf.read()

    fqn = get_fully_qualified_name("fit", code)
    assert fqn == "sklearn.pipeline.Pipeline.fit"


def test_fqn_code_snippet_39():
    with open(os.path.join(code_path, "39_seaborn_countplot.py")) as cf:
        code = cf.read()

    fqn = get_fully_qualified_name("Graph", code)
    assert fqn == "networkx.Graph"

    fqn = get_fully_qualified_name("add_edges_from", code)
    assert fqn == "networkx.Graph.add_edges_from"


def test_fqn_code_snippet_3010():
    with open(os.path.join(code_path, "3010_numpy_copyto.py")) as cf:
        code = cf.read()

    fqn = get_fully_qualified_name("seed", code)
    assert fqn == "numpy.random.seed"

    fqn = get_fully_qualified_name("rand", code)
    assert fqn == "numpy.random.rand"

    fqn = get_fully_qualified_name("randint", code)
    assert fqn == "numpy.random.randint"

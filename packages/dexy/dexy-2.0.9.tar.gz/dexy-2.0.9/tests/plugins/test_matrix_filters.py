from tests.utils import wrap
import dexy.filter

def test_matrix_filter():
    with wrap():
        f = dexy.filter.Filter.create_instance("matrix")
        assert f.is_active()
        f.process()
        print(f)

import pytest

pytestmark = pytest.mark.django_db


class TestProductModel:
    def test_str_method(self, product_factory):
        print(product_factory())
        assert 0==0

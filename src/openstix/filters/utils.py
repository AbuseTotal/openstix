from openstix.filters import Filter
from openstix.utils.extras import generate_possibilities


def generate_filters_with_name_and_alias(base_filter, name):
    possibilities = generate_possibilities(name)
    filter_by_name = [base_filter, Filter("name", "in", possibilities)]
    filter_by_alias = [base_filter, Filter("aliases", "in", possibilities)]
    return filter_by_name, filter_by_alias

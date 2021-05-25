from django import template

register = template.Library()

def paginator(context, adjacent_pages=2):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.

    """
    startPage = max(context['page_obj'].number - adjacent_pages, 1)
    if startPage <= 3: startPage = 1
    endPage = context['page_obj'].number + adjacent_pages + 1
    if endPage >= context['page_obj'].paginator.num_pages - 1: endPage = context['page_obj'].paginator.num_pages + 1
    page_numbers = [n for n in range(startPage, endPage) \
            if n > 0 and n <= context['page_obj'].paginator.num_pages]
    page_obj = context['page_obj']
    paginator = context['page_obj'].paginator

    return {
        'page_obj': page_obj,
        'paginator': paginator,
        # 'hits': context['hits'],
        # 'results_per_page': context['page_obj'].paginator.results_per_page,
        'page': context['page_obj'].number,
        'pages': context['page_obj'].paginator.num_pages,
        'page_numbers': page_numbers,
        'next': context['page_obj'].next_page_number,
        'previous': context['page_obj'].previous_page_number,
        'has_next': context['page_obj'].has_next,
        'has_previous': context['page_obj'].has_previous,
        'show_first': 1 not in page_numbers,
        'show_last': context['page_obj'].paginator.num_pages not in page_numbers,
    }

register.inclusion_tag('paginator.html', takes_context=True)(paginator)
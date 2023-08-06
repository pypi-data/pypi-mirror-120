def global_context(request, page):
    from garpix_menu.context_processors import menu_processor
    menus = menu_processor(request)
    return {
        'menus': menus['menus'],
    }

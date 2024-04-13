from django.http import HttpRequest

def menu_items(request: HttpRequest):
    schema_link = {
        'href': "/schema",
        'text': "Data schema",
        'active': request.path == "/schema"
    }

    sign_out_link = {
        "href": "/sign-out",
        "text": "Sign out",
        "active": False
    }

    sign_in_link = {
        "href": "/sign-in",
        "text": "Sign in",
        "active": request.path == "/sign-in"
    }

    sign_in_out_link = sign_out_link if request.user.is_authenticated else sign_in_link

    return { "menu_items": [schema_link, sign_in_out_link] }

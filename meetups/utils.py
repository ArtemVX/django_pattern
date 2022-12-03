menu_Authenticated = [
    {'title': 'Add meetup', 'url_name': 'new-meetup', 'class_name': 'left'},
    {'title': 'My account', 'url_name': 'profile', 'class_name': 'right'},
    {'title': 'Logout', 'url_name': 'logout', 'class_name': 'right'},
]

menu_unAuthenticated = [
    {'title': 'Login', 'url_name': 'login', 'class_name': 'left'},
    {'title': 'Register', 'url_name': 'register', 'class_name': 'right'},
]


class DataMixin:
    def get_user_context(self,  **kwargs):
        context = kwargs

        if self.request.user.is_authenticated:
            user_menu = menu_Authenticated
            user_menu[1]["title"] = self.request.user.username
            user_menu[1]["slug"] = self.request.user.pk

        else:
            user_menu = menu_unAuthenticated

        context['menu'] = user_menu
        return context

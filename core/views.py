from django.views.generic import TemplateView
from core.models import CloudApp
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response


# View for creating new apps
class AppView(APIView):

    def post(self, request, name):
        app = CloudApp(name=name)
        app.save()
        return Response({"id": app.key})


class AppListView(APIView):

    def get(self, request):
        app_props = ['name', 'key']
        app_list = []
        apps = CloudApp.objects.all()
        for app in apps:
            new_app = {}
            for prop in app_props:
                new_app[prop] = getattr(app, prop)
            app_list.append(new_app)
        return Response({'result': app_list})


class AccountKeysView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(AccountKeysView, self).get_context_data(**kwargs)
        apps = CloudApp.objects.all()
        context['apps'] = apps
        try:
            token = Token.objects.get(user=self.request.user)
            context['api_key'] = token.key
        except Token.DoesNotExist, e:
            context['api_key'] = ''
        return context

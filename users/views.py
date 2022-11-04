import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from avito.settings import TOTAL_ON_PAGE
from users.models import User, Location


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(self, request, *args, **kwargs)

        self.object_list = self.object_list.annotate(ads=Count('ad'))  # подсчёт объявлений для автора
        self.object_list = self.object_list.prefetch_related('locations').order_by('username')  # сортировка авторов

        paginator = Paginator(object_list=self.object_list, per_page=TOTAL_ON_PAGE)
        page_number = request.GET.get('page', 1)
        page_object = paginator.get_page(page_number)

        users = []
        for user in page_object:
            users.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "age": user.age,
                "locations": list(map(str, user.locations.all())),
                "total_ads": user.ads,
            })

        response = {'items': users,
                    "total": paginator.count,
                    'num_pages': paginator.num_pages
                    }

        return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "password": user.password,
            "role": user.role,
            "age": user.age,
            "locations": list(map(str, user.locations.all()))
        }, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'role', 'age', 'locations']

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(
            username=user_data["username"],
            password=user_data["password"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            role=user_data['role'],
            age=user_data['age'],
        )

        for i in user_data['locations']:
            location_obj, created = Location.objects.get_or_create(name=i, defaults={'lat': '0.001', 'lng': '0.002'})
            user.locations.add(location_obj)

        try:
            user.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            'age': user.age,
            "locations": list(map(str, user.locations.all()))
        }, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'role', 'age', 'locations']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)

        self.object.username = user_data["username"]
        self.object.password = user_data["password"]
        self.object.first_name = user_data["first_name"]
        self.object.last_name = user_data['last_name']
        self.object.role = user_data['role']
        self.object.age = user_data['age']

        for i in user_data['locations']:
            try:
                location_obj = Location.objects.get(name=i)
            except Location.DoesNotExist:
                return JsonResponse({'error': 'location not found'}, status=404)
            self.object.locations.add(location_obj)

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "username": self.object.username,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "role": self.object.role,
            'age': self.object.age,
            "locations": list(map(str, self.object.locations.all()))
        }, json_dumps_params={"ensure_ascii": False}
        )


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(self, request, *args, **kwargs)

        return JsonResponse({
            "status": 'ok'
        })

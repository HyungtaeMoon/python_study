### ViewSets

라우팅에서 요청에 사용할 컨트롤러를 결정한 후에 컨트롤러는 요청을 이해하고 적절한 출력을 생성해야 합니다. - Ruby on Rails Documentation

Django REST 프레임워크를 사용하면 `ViewSet` 이라고 하는 단일 클래스에서 관련 뷰 집합에 대한 논리를 결합할 수 있습니다. 다른 프레임 워크에서는 개념적으로 '자원' 또는 '컨트롤러'와 같은 이름의 구현을 찾을 수도 있습니다.


`ViewSet` 클래스는 `.get()` 이나 `.post()` 와 같은 메서드 핸들러를 제공하지 않고 단순히 `.list()` 및 `.create()` 와 같은 액션을 제공하는 클래스 기반 View 유형입니다.

ViewSet 메서드 핸들러는 `.as_view()` 메서드를 사용하여 View 를 마무리 할 시점의 해당 액션에만 바인딩 됩니다.

오히려 명시적으로 urlconf 의 ViewSet 의 View 를 등록하는 것보다, 자동으로 urlconf 를 결정하고, router class 가 있는 viewset 을 등록할 수 있습니다.

### Example

시스템의 모든 사용자를 나열하거나 검색하는데 사용할 수 있는 간단한 ViewSet 을 정의

```
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from myapps.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response

class UserViewSet(viewsets.ViewSet):
	"""
	A simple ViewSet for listing or retrieving users.
	"""
	def list(self, request):
		queryset = User.objects.all()
		serializer = UserSerializer(queryset, many=True)
		return Response(serializer.data)
		
	def retrieve(self, request, pk=None):
		queryset = User.objects.all()
		user = get_object_or_404(queryset, pk=pk)
		serializer = UserSerializer(user)
		return Response(serializer.data)
```

필요한 경우 이 viewset 을 다음과 같이 2개의 별도 view 에 바인딩할 수 있습니다.

```
user_list = UserViewSet.as_view({'get': 'list'})
user_detail = UserViewSet.as_view({'get': 'retrieve'})
```

ViewSet 을 router 에 등록하고 urlconf 가 자동으로 생성되도록 할 것입니다.

```
from myapp.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = router.urls
```

자신만의 viewsets 을 작성하는 대신 기본 동작 집합을 제공하는 기존 기본 클래스를 사용하는 것이 좋습니다.

```
class UserViewSet(viewsets.ModelViewSet):
	"""
	A viewset for viewing and editing user instances.
	"""
	serializer_class = UserSerializer
	queryset = User.objects.all()
```

View Class 를 사용하는 것보다 ViewSet Class 를 사용하는 두 가지 주요 이점이 있습니다.

- 반복 논리를 하나의 클래스로 결합할 수 있습니다. 위의 예에서 `queryset 을 한 번만 지정하면 여러 보기에서 사용됩니다.
- router 를 사용함으로써 우리는 URL conf 의 연결을 처리할 필요가 없습니다.

이 2가지 모두 절충안과 함께 제공됩니다. regular views 와 URL 구성을 사용하면 보다 명확하게 제어할 수 있습니다. ViewSet 은 신속하게 시작하고 실행하려는 경우, 또는 대규모 API 가 있고 전체적으로 일관된 URL 구성을 적용하려는 경우 유용합니다.


### ViewSet actions

REST 프레임워크에 포함 된 기본 라우터는 아래와 같이 표준 create/retrieve/update/destroy 스타일 액션 집합에 대한 경로를 제공합니다.

```
class UserViewSet(viewsets.ViewSet):
	"""
	Example empty viewset demonstrating the standard actions that will be handled by a router class.
	If you're using format suffixes, make sure to also include the 'format=None' keyword argument for each action.

def list(self, request):
	pass
	
def create(self, request):
	pass
	
def retrieve(self, request, pk=None):
	pass
	
def update(self, request, pk=None):
	pass
	
def partial_update(self, request, pk=None):
	pass
	
def destroy(self, request, pk=None):
	pass	

```


### Introspecting ViewSet actions

dispatch 하는 동안 `ViewSet 에서 다음 속성을 사용할 수 있습니다.

- `basename` - 작성된 URL 명에 사용
- `action` - 현재 action 의 이름(예: list, create)
- `detail` - 현재 list 또는 detail view 로 설정되어 있는지 나타냄
- `suffix` - viewset 유형의 display suffix - `detail` 속성을 미러링
- `name` - viewset 의 표시 이름. 이 argument 는 접미사와 상호 배타적
- `description` - viewset 의 개별 view 에 대한 표시 설명

이러한 속성을 검사하여 현재 작업을 기반으로 동작을 조정할 수 있습니다. 예를 들어 다음과 비슷한 `list` action 을 제외한 모든 권한을 제한할 수 있습니다.

```
def get_permission(self):
	"""
	Instantiates and returns the list of permissions that this view requires.
	"""
	if self.action == 'list':
		permission_classes = [IsAuthenticated]
	else:
		permission_classes = [IsAdmin]
	return [permission() for permission in permission_classes]
```

### Marking extra actions for routing

routing 이 가능한 특수한 메소드가 있다면 `@action` 데코레이터로 그 메서드를 표시할 수 있습니다. 일반 작업과 마찬가지로 추가 작업은 단일 개체 또는 전체 컬렉션을 대상으로 할 수 있습니다. 이를 나타내려면 `detail` 인수를 `True` 또는 `False` 로 설정하십시오. 라우터는 그에 따라 URL 패턴을 구성합니다. 예를들어 `DefaultRouter` 는 URL 패턴에 `pk`가 포함되도록 세부 동작을 구성합니다.

```
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from myapp.serializers import UserSerializer, PasswordSerializer

class UserViewSet(viewsets.ModelViewSet):
	"""
	A viewset that provides the standard actions
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer
	
	@action(detail=True, methods=['post'])
	def set_password(self, request, pk=None):
	user = self.get_object()
	serializer = PasswordSerializer(data=request.data)
	if serializer.is_valid():
		user.set_password(serializer.data['password']
		user.save()
		return Response({'status': 'password set'})
	else:
		return Response(serializer.errors, status=status.HTTP_400_BASE_REQUEST)
		
	@action(detail=False)
	def recent_users(self, request):
		recent_users = User.objects.all().order_by('-last_login')
		
		page = self.paginate_queryset(recent_users)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		
		serializer = self.get_serializer(recent_users, many=True)
		return Response(serializer.data)
	
```

데코레이터는 route 된 view 에 대해서만 arguments 를 추가로 취할 수 있습니다.

```
@action(detail=True, methods=['post'], permission_classes=[IsAdminOrIsSelf]
def set_password(self, request, pk=None):
	...
```

`action` 데코레이터는 기본적으로 GET 요청을 route 하지만 `methods 인수를 설정하여 다른 HTTP 메서드를 채택할 수도 있습니다.

```
@action(detail=True, methods=['post', 'delete'])
def unset_password(self, request, pk=None):
	...
```

이 2개의 새로운 action 은 `^users/{pk}/set_password/$` and `^users/{pk}/unset_password` 에서 사용할 수 있습니다.

추가 작업을 모두 보려면 `.get_extra_actions()` 메서드를 호출하십시오.

...
(중간 내용은 나중에 번역)


### Custom ViewSet base classes

`ModelViewSet` action 의 the full set of ModelViewSet actions 가 없거나 다른 방식으로 사용자를 정의해야 하는 경우에는 커스텀 `ViewSet 을 제공해야 할 수도 있습니다.

`create`, `list` 그리고 `retrieve` 조작을 제공하고 `GenericViewSet` 에서 상속하며 필요한 조치를 혼합하는 base viewset 클래스를 작성하려면 다음을 수행하십시오.

```
from rest_framework import mixins

class CreateListRetrieveViewSet(mixinis.CreateModelMixin,
									mixins.ListModelMixin,
									mixins.RetrieveModelMixin,
								 	viewsets.GenericViewSet):

	"""
	A viewset that provides 'retrieve', 'create', and 'list' actions.
	
	To use it, ovveride the class and set the '.queryset' and
	'.serializer_class' attributes.
	pass
```

고유한 기본 `ViewSet` 클래스를 작성하여 API 전반에 걸쳐 여러 viewsets 에서 재사용할 수 있는 공통적인 behavior 를 제공할 수 있습니다.


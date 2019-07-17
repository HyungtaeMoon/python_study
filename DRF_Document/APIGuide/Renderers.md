### Rednerers

TemplateResponse 인스턴스가 클라이언트에 반환되기 전에 렌더링되어야 합니다. 렌더링 프로세스는 템플릿과 컨텍스트의 중간 표현을 가져와서 클라이언트에 제공할 수 있는 최종 바이트 스트림으로 변환합니다.

REST 프레임워크에는 다양한 미디어 유형의 응답을 반환할 수 있는 여러 가지 `Renderer`클래스가 포함되어 있습니다. 또한 사용자 지정 렌더러를 정의할 수 있으므로 자신의 미디어 유형을 유연하게 디자인할 수 있습니다.

### How the renderer is determined

뷰에 유효한 렌더러 세트는 항상 클래스 목록으로 정의됩니다. view 가 입력되면 REST 프레임워크는 들어오는 요청에 대한 `content negotiation `을 수행하고 request 를 충족시키는 가장 적합한 렌더러를 결정합니다.

content negotiation 의 기본 프로세스는 요청의 수락 헤더를 검사하여 응답에서 예상되는 미디어 유형을 결정하는 것입니다. 선택적으로 URL 의 suffixes(접미사들)을 사용하여 명시적으로 특정 표현을 요청할 수 있습니다. 예를들어 `http://example.com/api/users_count.json` 은 항상 JSON 데이터를 반환하는 endpoint 일 수 있습니다. (content negotiaion 문서 참고)

### Setting the renderers

기본 렌더러 세트는 `DEFAULT_RENDERER_CLASSES` 설정을 사용하여 전역으로 설정할 수 있습니다. 예를 들어, 다음 설정은 `JSON`을 기본 미디어 유형으로 사용하며 자체 기술 API 도 포함합니다.

```
REST_FRAMEWORK = {
	'DEFAULT_RENDERER_CLASSES': (
		'rest_framework.renderers.JSONRenderer',
		'rest_framework.renderers.BrowsableAPIRenderer',
	)
}	
```

`APIView` 클래스 기반 view 를 사용하여 개별보기(individual view) 또는 viewset 에 사용되는 렌더러를 설정할 수도 있습니다.

```
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

class UserCountView(APIView):
	"""
	A view that returns the count of active users in JSON.
	"""
	renderer_classes = (JSONRenderer, )
	
	def get(self, request, format=None):
		user_count = User.objects.filter(active=True).count()
		content = {'user_count': user_count}
		return Response(content)
```

또는 `@api_view` 데코레이터를 사용하여 설정할 수도 있습니다.

```
@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def user_count_view(request, format=None):
	"""
	A view that returns the count of active users in JSON.
	"""
	user_count = User.objects.filter(active=True).count()
	content = {'user_count': user_count}
	return Response(content)

```

### Ordering of renderer classes

API 의 렌더러 클래스를 지정하여 각 미디어 유형에 할당 할 우선 순위를 생각할 때 중요합니다. 클라이언트가 `Accept: */*` 헤더를 보내는 것과 `Accept` 헤더를 포함하지 않는 것 같은 받아들일 수 있는 표현을 클라이언트가 명시하지 않으면 REST 프레임워크는 목록에서 응답에 사용할 첫 번째 렌더러를 선택합니다.

예를들어, API 가 JSON 응답과 HTML 탐색 가능한 API 를 제공하는 경우 Accept 헤더를 지정하지 않은 클라이언트에 JSON 응답을 보내려면 JSONRenderer 를 기본 렌더러로 설정하는 것이 좋습니다.

API 에 요청에 따라 일반 웹 페이지와 API 응답을 모두 제공할 수 있는 보기가 포함되어 있는 경우 깨진 수락 헤더(broken accept headers)를 보내는 이전 브라우저에서 제대로 재생하려면 `TemplateHTMLRenderer`를 기본 렌더러로 설정하는 것이 좋습니다.

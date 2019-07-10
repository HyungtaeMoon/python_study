### Responses

기본 HttpResponse 객체와 달리 TemplateResponse 객체는 응답을 계산하기 위해 view 에서 제공한 context 의 세부 정보를 유지합니다. 응답의 최종 출력은 나중에 필요할 때까지 계산되지 않고 나중에 응답 프로세스에서 계산됩니다. - Django documentation

REST framework 는 클라이언트 요청에 따라 여러 컨텐츠 형식으로 렌더링 할 수 있는 컨텐츠를 반환할 수 있게 해주는 `Response` 클래스를 제공하여 HTTP 컨텐츠 협상을 지원합니다.

`Response` 클래스는 Django 의 `SimpleTemplateResponse` 하위 클래스입니다. `Response objects` 는 원시 Python 기본 요소로 구성되어야하는 데이터로 초기화됩니다. 그런 다음 REST framework 는 표준 HTTP 내용 협상을 사용하여 최종 응답을 렌더링하는 방법을 결정합니다.

`Response` 클래스를 사용할 필요는 없으며 필요에 따라 view 에서 일반 `HttpResponse` 또는 `StreamingHttpResponse` 객체를 반환할 수도 있습니다. `Response` 클래스를 사용하면 여러 형식으로 렌더링할 수 있는 컨텐츠 협상 웹 API 응답을 반환하기에 더 좋은 인터페이스만 제공됩니다.

어떤 이유로든 REST framework 를 많이 사용자 정의하지 않으려면 `Response` 객체를 반환하는 view 에 항상 APIView 클래스 또는 @api_view 함수를 사용해야 합니다. 이렇게하면 view 에서 content negotiation 을 수행하고 응답에 적합한 렌더러를 선택하여 보기에서 반환할 수 있습니다.

### Creating responses

#### Response()

**Signature**: `Response(data, status=None, tempalte_name=None, headers=None, content_type=None)`

일반 `HttpResponse` 객체와 달리 렌더링 된 컨텐츠로 `Response` 객체를 인스턴스화하지 않습니다. 대신 파이썬 기본 요소로 구성되어 있는 렌더링되지 않은 데이터를 전달합니다.

`Reponse` 클래스에서 사용하는 렌더러는 Django 모델 인스턴스와 같은 복잡한 유형을 기본적으로 처리할 수 없으므로 `Response` 객체를 만들기 전에 데이터를 원시 데이터 유형으로 직렬화해야 합니다.

REST framework 의 `Serializer` 클래스를 사용하여 이 데이터 직렬화를 수행하거나 사용자 정의 직렬화를 사용할 수 있습니다.

Arguments:

- `data`: 응답의 직렬화 된 데이터입니다.
- `status`: 응답의 상태 코드입니다. 기본값은 200입니다.
- `template_name`: `HTMLRenderer` 를 선택한 경우 사용할 템플릿 이름입니다.
- `headers`: 응답에 사용할 HTTP 헤더 사전입니다.
- `content_type`: 응답의 컨텐츠 유형입니다. 일반적으러 content negotiation 에 의해 결정되는 렌더러에 의해 자동으로 설정되지만 내용 유형을 명시적으로 지정해야 하는 경우가 많습니다.
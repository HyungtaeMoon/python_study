### Exceptions

Exceptions....프로그램 구조 내의 중앙 또는 상위 위치에서 오류 처리를 명확하게 구성할 수 있습니다.

### Exception handling in REST framework views

REST 프레임워크의 뷰는 다양한 예외를 처리하고 적절한 오류 응답을 반환합니다.

처리되는 예외는 다음과 같습니다.

- REST 프레임 워크 내에서 발생하는 `APIException` 의 서브 클래스입니다.
- 장고의 `Http404` exception
- 장고의 `PermissionDenied` exception

각각의 경우에 REST 프레임워크는 적절한 상태 코드 및 내용 유형이 포함 된 응답을 반환합니다. 응답 본문에는 오류의 성격과 관련된 추가 세부 정보가 포함됩니다.

대부분의 오류 응답에는 응답 본문의 `detail`이 포함됩니다.(Most error responses will include a key detail in the body of the response)

예를 들면 아래와 같습니다.

```
DELETE http://api.example.com/foo/bar HTTP/1.1
Accept: application/json
```

해당 리소스에서 `DELETE` 메서드가 허용되지 않는다는 오류 응답을 받을 수 있습니다.

```
HTTP/1.1 405 Method Not Allowed
Content-Type: application/json
Content-Length: 42

{"detail": "Method 'DELETE' not allowed."}
```

유효성 검사 오류는 약간 다르게 처리되며 필드 이름을 응답의 키로 포함합니다. 유효성 검사 오류가 특정 필드에만 해당되지 않으면 "non_field_errors" 키를 사용하거나 `NON_FIELD_ERRORS_KEY` 설정에 대해 설정된 문자열 값을 사용합니다.

모든 유효성 검증 오류는 다음과 같습니다.

```
HTTP/1.1 400 Bad Request
Content-Type: application/json
Content-Length: 94

{"amount": ["A valid integer is required."], "description": ["This field may not be blank."]
```

### Custom exception handling

생략

### API Reference

APIException

`APIException`

`APIView` 클래스 또는 `@api_view` 내부에서 발생한 모든 예외에 대한 기본 클래스입니다.

사용자 정의 예외를 제공하려면 `APIException`을 서브 클래스 화하고 클래스의 `.status_code`, `default_detail` 및 `default_code` 속성을 설정하십시오.

예를들어, API 가 가끔 도달할 수 없는 제 3자 서비스에 의존하는 경우 "503 서비스를 사용할 수 없음" HTTP 응답 코드에 대한 예외를 구현할 수 있습니다. 이렇게 할 수 있습니다.

```
from rest_framework.exceptions import APIException

class ServiceUnavailable(APIException):
	status_code = 503
	default_detail = 'Service temparly unavailable, try again later.'
	default_code = 'service_unavailable'
```

#### inspecting API exceptions

API 예외 상태를 검사하는데 사용할 수 있는 여러 가지 등록 정보가 있습니다. 이를 사용하여 프로젝트에 대한 사용자 정의 예외 처리를 빌드할 수 있습니다.

이용할 수 있는 속성과 메서드는 다음과 같습니다.

`.detail` - 오류의 텍스트 설명을 리턴
`.get_codes()` - 오류의 코드 식별자를 반환
`.get_full_details()` - 오류의 텍스트 설명과 코드 식별자를 반환


생략
...

###ValidationError

`ValidationError(detail, code=None)`

`ValidationError` 예외는 다른 `APIException` 클래스와 약간 다릅니다.

- `detail` 은 필수 항목입니다.(not optional)
- `detail` 인수는 오류 세부 정보 목록 또는 dict 일 수 있으며 중첩 된 데이터 구조일 수 있습니다.
- 규칙에 따라 serializer 모듈을 가져와 정규화 된 ValidationError 스타일을 사용하여 Django 의 기본 유효성 검사 오류와 구별해야 합니다. 예를들어 serializer 를 올립니다. ValidationError('이 필드는 정수 값이어야 합니다')

`ValidationError` 클래스는 serializer 및 필드 유효성 검사 및 유효성 검사기 클래스에 사용해야 합니다. 또한 raise_exception 키워드 인수로 `serializer.is_valid` 를 호출할 때 발생합니다.

```
serializer.is_valid(raise_exception=True)
```


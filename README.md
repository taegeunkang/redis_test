# AWS MemoryDB 클러스터 접속 예제

이 프로그램은 Python 3.11을 사용하여 AWS MemoryDB 클러스터에 접속하는 예제를 제공합니다.

## 필수 요구사항

- Python 3.11 이상
- AWS MemoryDB 클러스터가 생성되어 있어야 함
- 클러스터 엔드포인트 및 접속 정보 필요

## 설치 방법

1. 필요한 패키지 설치:

```bash
pip install -r requirements.txt
```

## 사용 방법

1. `main.py` 파일에서 다음 정보를 수정하세요:
   - `endpoint`: MemoryDB 클러스터 엔드포인트 주소
   - `port`: 포트 번호 (기본값: 6379)
   - `username`: 사용자명 (ACL이 활성화된 경우)
   - `password`: 비밀번호 (인증이 필요한 경우)

2. 스크립트 실행:

```bash
python main.py
```

## 주요 기능

- MemoryDB 클러스터에 SSL을 통한 안전한 연결
- 기본적인 키-값 쓰기/읽기 기능
- TTL(Time-To-Live) 설정 기능
- 데이터 삭제 기능
- 오류 처리 및 로깅

## 코드 구조

- `MemoryDBClient` 클래스: MemoryDB 클러스터 연결 및 작업 수행
  - `connect()`: 클러스터에 연결
  - `set_value()`: 키-값 저장
  - `get_value()`: 키에 해당하는 값 조회
  - `delete_key()`: 키 삭제
  - `close()`: 연결 종료

## 주의사항

- 실제 운영 환경에서는 비밀번호를 코드에 직접 입력하지 말고 환경 변수나 AWS Secrets Manager 등을 사용하세요.
- 프로덕션 환경에서는 연결 풀링, 재시도 로직 등 추가 기능을 고려하세요. 
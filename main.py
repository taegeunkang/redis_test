import redis
import ssl
import logging
from typing import Optional

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MemoryDBClient:
    def __init__(
        self,
        endpoint: str,
        port: int = 6379,
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_ssl: bool = True,
        db: int = 0,
    ):
        """
        AWS MemoryDB 클라이언트 초기화

        Args:
            endpoint: MemoryDB 클러스터 엔드포인트
            port: 포트 번호 (기본값: 6379)
            username: 사용자명 (ACL 활성화 시)
            password: 비밀번호
            use_ssl: SSL 사용 여부 (기본값: True)
            db: 사용할 데이터베이스 번호 (기본값: 0)
        """
        self.endpoint = endpoint
        self.port = port
        self.username = username
        self.password = password
        self.use_ssl = use_ssl
        self.db = db
        self.connection = None

    def connect(self):
        """MemoryDB 클러스터에 연결"""
        try:
            # SSL 설정
            ssl_context = ssl.create_default_context() if self.use_ssl else None

            # 연결 설정
            connection_args = {
                "host": self.endpoint,
                "port": self.port,
                "db": self.db,
                "decode_responses": True,  # 응답을 문자열로 디코딩
            }

            # 인증 정보 추가
            if self.username and self.password:
                connection_args["username"] = self.username
                connection_args["password"] = self.password
            elif self.password:
                connection_args["password"] = self.password

            # SSL 설정 추가
            if self.use_ssl:
                connection_args["ssl"] = True
                # connection_args["ssl_context"] = ssl_context

            # 연결 생성
            self.connection = redis.Redis(**connection_args)

            # 연결 테스트
            self.connection.ping()
            logger.info(
                f"MemoryDB 클러스터 {self.endpoint}:{self.port}에 성공적으로 연결되었습니다."
            )
            return True

        except redis.exceptions.ConnectionError as e:
            logger.error(f"연결 오류: {e}")
            return False
        except Exception as e:
            logger.error(f"예상치 못한 오류: {e}")
            return False

    def set_value(self, key: str, value: str, ttl: Optional[int] = None) -> bool:
        """
        키-값 쌍을 저장

        Args:
            key: 키
            value: 값
            ttl: 만료 시간 (초)

        Returns:
            성공 여부
        """
        try:
            if ttl:
                return self.connection.setex(key, ttl, value)
            return self.connection.set(key, value)
        except Exception as e:
            logger.error(f"값 설정 오류: {e}")
            return False

    def get_value(self, key: str) -> Optional[str]:
        """
        키에 해당하는 값 조회

        Args:
            key: 키

        Returns:
            값 또는 키가 없는 경우 None
        """
        try:
            return self.connection.get(key)
        except Exception as e:
            logger.error(f"값 조회 오류: {e}")
            return None

    def delete_key(self, key: str) -> bool:
        """
        키 삭제

        Args:
            key: 삭제할 키

        Returns:
            성공 여부
        """
        try:
            return bool(self.connection.delete(key))
        except Exception as e:
            logger.error(f"키 삭제 오류: {e}")
            return False

    def close(self):
        """연결 종료"""
        if self.connection:
            self.connection.close()
            logger.info("MemoryDB 연결이 종료되었습니다.")


def main():
    # 클러스터 정보 설정
    endpoint = (
        "clustercfg.healthier-demo-redis.m95rrh.memorydb.ap-northeast-2.amazonaws.com"
    )
    port = 6379
    # 인증 정보 설정 (필요한 경우)
    username = None  # ACL이 활성화된 경우 사용자명 설정
    password = None  # 암호 인증을 사용하는 경우 설정

    # 클라이언트 초기화 및 연결
    client = MemoryDBClient(
        endpoint=endpoint, port=port, username=username, password=password, use_ssl=True
    )

    if not client.connect():
        logger.error("MemoryDB 클러스터 연결에 실패했습니다.")
        return

    try:
        # 키-값 쓰기
        client.set_value("test_key", "Hello MemoryDB!")
        logger.info("데이터 쓰기 완료")

        # 키-값 읽기
        value = client.get_value("test_key")
        logger.info(f"test_key의 값: {value}")

        # TTL로 키-값 쓰기
        client.set_value("temp_key", "임시 데이터", ttl=60)  # 60초 후 만료
        logger.info("60초 후 만료되는 임시 데이터 저장 완료")

        # 키 삭제
        if client.delete_key("test_key"):
            logger.info("test_key 삭제 완료")

    finally:
        # 연결 종료
        client.close()


if __name__ == "__main__":
    main()

import os


class EnvValue:
    LOCAL: str = "local"
    TEST: str = "test"
    PRE: str = "pre"
    PROD: str = "prod"


class Env:
    @property
    def env(self) -> str:
        return os.getenv("ENV", EnvValue.LOCAL).lower()

    def is_prod(self) -> bool:
        return self.env == EnvValue.PROD

    def is_pre(self) -> bool:
        return self.env == EnvValue.PRE

    def is_local(self) -> bool:
        return self.env == EnvValue.LOCAL

    def is_test(self) -> bool:
        return self.env == EnvValue.TEST

    @staticmethod
    def is_k8s() -> bool:
        if os.getenv("KUBERNETES_SERVICE_HOST"):
            return True

        if os.path.isfile("/var/run/secrets/kubernetes.io/serviceaccount/token"):
            return True

        return False

    def __str__(self):
        return self.env


env = Env()

__all__ = ["env"]

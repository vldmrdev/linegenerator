import random

from linegenerator.core.provider import BaseProvider


#  TODO
class HttpProvider(BaseProvider):
    METHODS = ["GET", "POST", "PUT", "DELETE", "HEAD", "PATCH"]
    PATHS = ["/", "/api/users", "/login", "/health", "/static/style.css", "/api/orders", "/profile"]
    STATUSES = {
        200: "OK",
        201: "Created",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        500: "Internal Server Error",
    }

    def _http_method(self):
        return random.choice(self.METHODS)

    def _uri_path(self):
        return random.choice(self.PATHS)

    def _http_status_code(self):
        return str(random.choice(list(self.STATUSES.keys())))

    def _status_text(self):
        code = random.choice(list(self.STATUSES.keys()))
        return self.STATUSES[code]

    def _response_size(self):
        return str(random.randint(0, 10240))

    def _safe_referer_url(self):
        return random.choice(["-", "https://example.com", "https://google.com/search?q=test"])

    def _user_agent(self):
        return random.choice(
            [
                "-",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                "curl/7.68.0",
                "python-requests/2.28.1",
            ]
        )

    def get_generators(self):
        return {
            "http_method": self._http_method,
            "uri_path": self._uri_path,
            "http_status_code": self._http_status_code,
            "status_text": self._status_text,
            "response_size": self._response_size,
            "size": self._response_size,  # alias for APACHE
            "safe_referer_url": self._safe_referer_url,
            "user_agent": self._user_agent,
            "method": self._http_method,  # alias for FASTAPI/APACHE
            "path": self._uri_path,  # alias for FASTAPI/APACHE
        }

from enum import StrEnum


class LogPreset(StrEnum):
    NGINX = '{ipv4_public} - - [{timestamp}] "{http_method} {uri_path} HTTP/1.1" {http_status_code} {response_size} "{safe_referer_url}" "{user_agent}"'

    POSTGRES = "{timestamp} [{pid}]: [1-1] user={user},db={db},app={app},client={client} LOG:  duration: {duration} ms  statement: {statement}"

    # FASTAPI = 'INFO:     {ip}:{port} - "{method} {path} HTTP/1.1" {status} {status_text}'
    # SSH_LOGIN_SUCCESS = "{month} {day} {time} server sshd[{pid}]: Accepted password for {user} from {ip} port {port} ssh2"
    # SSH_LOGIN_FAILED = "{month} {day:2} {time} server sshd[{pid}]: Failed password for {user} from {ip} port {port} ssh2"
    # SYSLOG_GENERIC = "{month} {day:2} {time} server {service}[{pid}]: {message}"
    # APACHE = '{ip} - {user} [{timestamp:%d/%b/%Y:%H:%M:%S +0000}] "{method} {path} HTTP/1.1" {status} {size}'

    @classmethod
    def get_preset(cls, name: str) -> "LogPreset":
        try:
            return cls[name.upper()]
        except KeyError:
            raise ValueError(f"Unknown preset '{name}'. Available: {cls.list_preset_names()}")

    @classmethod
    def list_preset_names(cls) -> list[str]:
        return [p.name.upper() for p in cls]

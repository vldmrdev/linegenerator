from enum import Enum


class AppsPresets(str, Enum):
    POSTGRES = "{timestamp} [{pid}]: [1-1] user={user},db={db},app={app},client={client} LOG:  duration: {duration} ms  statement: {statement}"
    NGINX = '{ip} - - [{timestamp:%d/%b/%Y:%H:%M:%S +0000}] "{method} {path} HTTP/1.1" {status} {size} "{referer}" "{user_agent}"'
    FASTAPI = 'INFO:     {ip}:{port} - "{method} {path} HTTP/1.1" {status} {status_text}'
    SSH_LOGIN_SUCCESS = "{month} {day} {time} server sshd[{pid}]: Accepted password for {user} from {ip} port {port} ssh2"
    SSH_LOGIN_FAILED = "{month} {day:2} {time} server sshd[{pid}]: Failed password for {user} from {ip} port {port} ssh2"
    SYSLOG_GENERIC = "{month} {day:2} {time} server {service}[{pid}]: {message}"
    APACHE = '{ip} - {user} [{timestamp:%d/%b/%Y:%H:%M:%S +0000}] "{method} {path} HTTP/1.1" {status} {size}'

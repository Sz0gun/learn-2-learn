FROM hashicorp/vault:latest

RUN mkdir -p /vault/config/certs

COPY config/vault.hcl /vault/config/vault.hcl
COPY certs/server.crt /vault/config/certs/server.crt
COPY certs/server.key /vault/config/certs/server.key

CMD ["vault", "server", "-config=/vault/config/vault.hcl"]

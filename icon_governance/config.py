from pydantic import BaseSettings


class Settings(BaseSettings):

    NAME: str = "governance"
    NETWORK_NAME: str = "mainnet"

    # Ports
    PORT: int = 8000
    HEALTH_PORT: int = 8180
    METRICS_PORT: int = 9400

    METRICS_ADDRESS: str = "localhost"

    # Prefix
    REST_PREFIX: str = "/api/v1"
    HEALTH_PREFIX: str = "/heath"
    METRICS_PREFIX: str = "/metrics"
    DOCS_PREFIX: str = "/api/v1/governance/docs"

    CORS_ALLOW_ORIGINS: str = "*"
    CORS_ALLOW_CREDENTIALS: bool = False
    CORS_ALLOW_METHODS: str = "GET,POST,HEAD,OPTIONS"
    CORS_ALLOW_HEADERS: str = ""
    CORS_EXPOSE_HEADERS: str = "x-total-count"

    # Monitoring
    HEALTH_POLLING_INTERVAL: int = 60

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_TO_FILE: str = "false"
    LOG_FILE_NAME: str = "governance.log"
    LOG_FORMAT: str = "string"

    # ICON Nodes
    ICON_NODE_URL: str = "https://api.icon.geometry.io/api/v3"
    BACKUP_ICON_NODE_URL: str = "https://ctz.solidwallet.io/api/v3"

    # Logs service - For getting value for iscore
    # TODO: Replace this when stateful processing comes in maybe
    LOGS_SERVICE_URL: str = "https://tracker.icon.community"

    # ICON Peers - Used to discover nodes across the network
    PEER_SEED_IP: str = "52.196.159.184"
    PEER_SEED_ADDRESS: str = "hx9c63f73d3c564a54d0eed84f90718b1ebed16f09"

    # Backfilling
    JOB_ID: str = None

    # Kafka
    KAFKA_BROKER_URL: str = "localhost:29092"
    SCHEMA_REGISTRY_URL: str = "http://localhost:8081"
    CONSUMER_IS_TAIL: bool = False

    KAFKA_GROUP_ID: str = "governance-service"

    # Topics
    CONSUMER_GROUP: str = "governance"
    SCHEMA_NAME_TOPICS: str = "governance-ws:block"

    CONSUMER_TOPIC_BLOCKS: str = "governance"
    CONSUMER_TOPIC_TRANSACTIONS: str = "transactions"
    CONSUMER_TOPIC_LOGS: str = "logs"

    # DB
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "changeme"
    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DATABASE: str = "postgres"

    # Endpoints
    MAX_PAGE_SIZE: int = 100

    # Redis
    # REDIS_HOST: str = "redis"
    # REDIS_PORT: int = 6379
    # REDIS_PASSWORD: str = ""
    # REDIS_CHANNEL: str = "governance"
    # REDIS_SENTINEL_CLIENT_MODE: bool = False
    # REDIS_SENTINEL_CLIENT_MASTER_NAME: str = "master"

    governance_address: str = "cx0000000000000000000000000000000000000000"

    CRON_SLEEP_SEC: int = 600

    PRODUCER_TOPIC_GOVERNANCE_PREPS: str = "governance-preps-processed"

    class Config:
        case_sensitive = True
        # env_prefix = "GOVERNANCE_"


settings = Settings()

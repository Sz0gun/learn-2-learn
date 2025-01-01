# FILE: event_handler.py
## Further Optimiations
1. Rate Limiting:
    - Add logic to limit message frequency per user or chat to avoid spamming
2. Compression
    - compress msg before storing in Redis
3. Background Task for Queuning
    - use "asyncio.create_task" for non-blocking Redis operations
4. Batch Processing
5. Telemetry
    - add logging or metrics collection for monitoring
## Scalability and Performance Gains

- Reduced Latency: Avoid processing unnecessary or empty messages.
- Fault Tolerance: Proper error handling ensures that errors don’t propagate or crash the bot.
- Queue Optimization: Using rpush ensures FIFO order, simplifying downstream processing.
- Rate Limiting: Protects against spamming or abusive behavior.

## Summary

To ensure data is safe during the transfer time:

- Enable TLS for Redis or route traffic through an SSH tunnel.
- Use authentication for Redis.
- Encrypt sensitive data before storing it in Redis.
- Avoid exposing Redis directly to the public internet.


plik main.py to jak szkic dla implementacji funkcji i pozniejszego nadania im miejsca tworzac folder/plik

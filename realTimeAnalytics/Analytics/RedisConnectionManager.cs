using StackExchange.Redis;

namespace Analytics;

public static class RedisConnectionManager
{
    public static ConnectionMultiplexer Connection { get; } = ConnectionMultiplexer.Connect("localhost");
}
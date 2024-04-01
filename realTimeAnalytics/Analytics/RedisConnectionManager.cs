using StackExchange.Redis;

namespace Analytics;

public static class RedisConnectionManager
{
    private static string GetConnectionString()
    {
        return $"{Environment.GetEnvironmentVariable("REDIS_HOST") ?? string.Empty},"
               + $"abortConnect={false},"
               + "connectRetry=5";
    }
    
    public static ConnectionMultiplexer Connection { get; } = ConnectionMultiplexer.Connect(GetConnectionString());
}
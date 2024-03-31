using Analytics.Options;
using Microsoft.Extensions.Options;
using NRedisStack;
using NRedisStack.RedisStackCommands;
using StackExchange.Redis;

namespace Analytics.Services;

internal abstract class BaseService : IAnalyticsService
{
    protected readonly ITimeSeriesCommands TimeSeriesDatabase;
    protected readonly IDatabase MetaDataDatabase;
    protected readonly RedisOptions RedisOptions;

    protected BaseService(IOptions<RedisOptions> redisOptions)
    {
        TimeSeriesDatabase = RedisConnectionManager.Connection.GetDatabase(redisOptions.Value.TimeSeriesDbIndex).TS();
        MetaDataDatabase = RedisConnectionManager.Connection.GetDatabase(redisOptions.Value.MetaDataDbIndex);
        RedisOptions = redisOptions.Value;
    }

    public abstract Task Execute(CancellationToken cancellationToken);
}
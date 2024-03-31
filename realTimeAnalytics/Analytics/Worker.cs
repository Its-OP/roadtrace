using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace Analytics;

public class Worker : BackgroundService
{
    private readonly ILogger<Worker> _logger;
    private readonly IServiceScopeFactory _serviceScopeFactory;

    public Worker(ILogger<Worker> logger, IServiceScopeFactory serviceScopeFactory)
    {
        _logger = logger;
        _serviceScopeFactory = serviceScopeFactory;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            _logger.LogInformation("Collecting analytics:");
            await using var scope = _serviceScopeFactory.CreateAsyncScope();
            var analyticsServices = scope.ServiceProvider.GetRequiredService<IEnumerable<IAnalyticsService>>();
            await Parallel.ForEachAsync(analyticsServices, stoppingToken, async (service, token) =>
            {
                try
                {
                    await service.Execute(token);
                }
                catch (Exception e)
                {
                    _logger.LogError(e, "Service {serviceName} thrown an exception during the execution", service.GetType().Name);
                }
            });

            await Task.Delay(100, stoppingToken);
        }
    }
}
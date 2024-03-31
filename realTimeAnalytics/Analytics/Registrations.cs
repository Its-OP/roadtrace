using Analytics.Options;
using Analytics.Services;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace Analytics;

public static class Registrations
{
    public static IServiceCollection RegisterAnalytics(this IServiceCollection services, IConfiguration configuration)
    {
        services.Configure<RedisOptions>(configuration.GetSection("Redis"));

        services.AddScoped<IAnalyticsService, NumberOfVehiclesService>();

        services.AddHostedService<Worker>();

        return services;
    }
}
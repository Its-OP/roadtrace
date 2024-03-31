using System.Text.Json;
using Analytics.Entities;
using Analytics.Options;
using Microsoft.Extensions.Options;

namespace Analytics.Services;

internal class NumberOfVehiclesService : BaseService
{
    private const double TimePeriod = 0.1;
    
    public NumberOfVehiclesService(IOptions<RedisOptions> redisOptions) : base(redisOptions)
    {
    }

    public override async Task Execute(CancellationToken cancellationToken)
    {
        if (cancellationToken.IsCancellationRequested)
            return;
        
        var frameIds = TimeSeriesDatabase.Range(RedisOptions.RtsKeyName, DateTime.Now.AddSeconds(-TimePeriod), DateTime.Now)
            .Select(x => Convert.ToInt32(x.Val));
        
        if (cancellationToken.IsCancellationRequested)
            return;
        
        var numberOfUniqueVehicles = (await Task.WhenAll(frameIds.Select(x => GetVehiclesByFrameId(x, cancellationToken))))
            .SelectMany(frameVehicles => frameVehicles.Select(vehicle => vehicle.TrackId))
            .Distinct()
            .Count();
        
        Console.WriteLine($"Number of unique vehicles: {numberOfUniqueVehicles}");
    }

    private async Task<IEnumerable<Vehicle>> GetVehiclesByFrameId(int frameId, CancellationToken token)
    {
        if (token.IsCancellationRequested)
            return [];
        
        var jsonVehicles = (await MetaDataDatabase.ListRangeAsync($"{RedisOptions.MetadataKeyPrefix}:{frameId}")).Select(x => x.ToString());
        if (token.IsCancellationRequested)
            return [];
        
        var vehicles = jsonVehicles
            .Select(x => JsonSerializer.Deserialize<Vehicle>(x))
            .Where(x => x is not null)
            .Select(x => x!);

        return vehicles;
    }
}
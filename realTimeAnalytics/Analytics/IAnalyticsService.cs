namespace Analytics;

public interface IAnalyticsService
{
    public Task Execute(CancellationToken cancellationToken);
}
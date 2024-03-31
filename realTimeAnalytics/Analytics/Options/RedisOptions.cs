namespace Analytics.Options;

public class RedisOptions
{
    public int TimeSeriesDbIndex { get; set; }
    public int MetaDataDbIndex { get; set; }
    public string RtsKeyName { get; set; } = string.Empty;
    public string MetadataKeyPrefix { get; set; } = string.Empty;
}
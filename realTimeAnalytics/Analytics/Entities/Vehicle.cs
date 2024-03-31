using System.Text.Json.Serialization;

namespace Analytics.Entities;

public record Vehicle([property:JsonPropertyName("track_id")] int TrackId, int X1, int Y1, int X2, int Y2);
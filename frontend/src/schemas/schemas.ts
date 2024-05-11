export interface Schemas {
    lng: number,
    lat: number
}

export interface Marker {
    id: number,
    coordinates: Schemas,
    dirty: boolean
}

export interface DataPoint {
    date: Date,
    value: number
}
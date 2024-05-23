export interface LatLong {
    lng: number,
    lat: number
}

export interface Marker {
    id: number,
    coordinates: LatLong,
    source: string,
    dirty: boolean
}

export interface DataPoint {
    date: Date,
    value: number
}

export interface User {
    email: string;
    role: string;
    password?: string;
    hasChanged?: boolean;
}

export const UserRoles = ['user', 'manager', 'administrator'];

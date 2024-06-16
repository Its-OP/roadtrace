export interface LatLong {
    lng: number,
    lat: number
}

export interface Marker {
    id: number,
    coordinates: LatLong,
    code: string,
    source: string,
    dirty: boolean,
    numbers: DataPoint[],
    velocities: DataPoint[]
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

export function sleep(milliseconds: number) {
    const start = Date.now();
    while (Date.now() - start < milliseconds) { }
}

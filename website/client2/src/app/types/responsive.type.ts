export class ResponsiveType {
    width: number = 0;
    height: number = 0;
    deviceType: DeviceType = DeviceType.Desktop;

    constructor(width: number, height: number) {
        this.width = width;
        this.height = height;
        this.setDeviceType(width);
    }

    setDeviceType = (width: number) => {
        if (width < 768) {
            this.deviceType = DeviceType.Mobile;
        } else if (width < 1024) {
            this.deviceType = DeviceType.Tablet;
        } else {
            this.deviceType = DeviceType.Desktop;
        }
    }
}

export enum DeviceType {
    Mobile = "mobile",
    Tablet = "tablet",
    Desktop = "desktop"
}

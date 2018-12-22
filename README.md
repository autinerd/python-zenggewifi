# Python control for Zengge Wi-Fi LED bulbs

## Example usage

### Connecting

```Python
import zenggewifi

bulb = zenggewifi.ZenggeWifiBulb('192.168.1.20')
bulb.connect()
```

### Get State

```Python
state = bulb.get_status()
```
Returns a status object which contains of these members:

```Python
state.deviceType # Type of device
state.isOn # whether device is on
state.Mode # current mode
state.Slowness # current slowness
state.Color # current color, color object
state.LedVersionNum # version of LED
```

### Set Color

```Python
bulb.set_on(color)
```

Color object has these members:

```Python
self.R # Red value [0-255]
self.G # Green value [0-255]
self.B # Blue value [0-255]
self.W # Warmwhite value [0-255]
self.IgnoreW # Whether warmwhite is ignored (then RGB is used) or not (then only warmwhite is used)
```

### Turn off

```Python
bulb.set_off()
```
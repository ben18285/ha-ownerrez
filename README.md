# Home Assistant - OwnerRez Integration

## Overview
This custom component integrates OwnerRez reservation data into Home Assistant, providing real-time check-out dates.

## Installation
1. Copy the `custom_components/ownerrez/` folder into your Home Assistant setup.
2. Restart Home Assistant.
3. Add the following to your `configuration.yaml`:
```yaml
ownerrez:
  api_key: "YOUR_OWNERREZ_API_KEY"
```
4. Restart Home Assistant again.

## Usage
- The integration provides a sensor `sensor.ownerrez_check_out_date` that updates based on the latest reservation check-out date.
- You can automate dashboard resets or other actions based on this sensor.

## License
GPL-3.0

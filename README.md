# Home Assistant - OwnerRez Integration

## Overview
This custom component integrates OwnerRez reservation data into Home Assistant, providing real-time check-out dates.

## Installation
1. Copy the `custom_components/ownerrez/` folder into your Home Assistant setup.
2. Restart Home Assistant.

## Configuration
- This integration **no longer uses YAML configuration**.
- Instead, go to **Settings > Devices & Services** in Home Assistant.
- Click **Add Integration** and search for **OwnerRez**.
- Enter your **OwnerRez API Key** when prompted.

## Usage
- The integration provides a sensor `sensor.ownerrez_check_out_date` that updates based on the latest reservation check-out date.
- You can automate dashboard resets or other actions based on this sensor.

## License
GPL-3.0

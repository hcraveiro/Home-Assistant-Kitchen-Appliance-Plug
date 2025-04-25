# Home Assistant Kitchen Appliance Plug Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)

Detect usage state of kitchen appliances such as dishwashers, blenders or cookers using a smart plug with power monitoring. This integration provides a virtual status sensor based on power consumption and optional idle delay.

- [Home Assistant Kitchen Appliance Plug Integration](#home-assistant-kitchen-appliance-plug-integration)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Entities](#entities)
  - [FAQ](#faq)

## Installation

This integration can be added as a custom repository in HACS. After installing it via HACS:

1. Go to **Settings → Devices & Services → Add Integration**.
2. Search for **Kitchen Appliance Plug**.
3. Follow the configuration wizard.

## Configuration

For each kitchen appliance you want to monitor, you must add a configuration entry. During the setup flow, you will be asked to provide:

- A name for the appliance.
- The power sensor entity associated with the plug.
- The minimum power threshold (in watts) to consider the appliance "active".
- The name of the active state (e.g. `Cooking`, `Washing`).
- An icon to represent the appliance status (used in the status sensor).
- The idle timeout (in seconds) to wait before considering the appliance turned off when power drops below the threshold.

All of these settings can be changed later via the **Configure** option in the integration.

## Entities

For each configured appliance, the integration creates:

- `sensor.<name>_status`: shows one of the following:
  - The custom state you configured (e.g. `Cooking`)
  - `Off`

This sensor is linked to the same device as the power sensor used for monitoring.

## FAQ

### How is the status determined?

The integration monitors the power sensor:
- If the power is greater than or equal to the configured threshold, the appliance is considered active.
- If the power falls below the threshold for longer than the idle timeout, the state changes to `Off`.

### What is the purpose of the idle timeout?

Many appliances briefly drop power between cycles. The idle timeout prevents false detection of shutdown during short pauses.

### Can I change the state label or icon later?

Yes. Use the **Configure** button in the integration panel to adjust settings including the display name, power threshold, icon, and idle timeout.

### Can I use this with multiple appliances?

Yes. You can add multiple config entries, one for each appliance, with separate power sensors and thresholds.

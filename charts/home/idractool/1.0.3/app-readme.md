# iDRAC Tools - Data Extractor and MQTT Publisher

[iDrac  Tools](https://github.com/martinikolaev/idrac-tools)

## Overview

This Python script is designed to interact with iDRAC interfaces via IPMI, extracting specific data based on environment variables, and then publishing this data to an MQTT broker. It's an effective tool for remotely monitoring and managing server health and status in real-time.

## Features

-   **iDRAC and IPMI Integration**: Connects to iDRAC interfaces using IPMI to fetch server data.
-   **Dynamic Data Retrieval**: Utilizes environment variables prefixed with `IDRAC_` to determine which data to request from the iDRAC interface.
-   **MQTT Publishing**: Sends the retrieved data to an MQTT broker, with each data point published under a topic corresponding to its environment variable.

## Requirements

-   Python environment capable of interfacing with IPMI and MQTT.
-   iDRAC interface accessible via IPMI.
-   Configured MQTT broker for data publishing.

## Configuration

1.  **iDRAC Parameters**: Specify iDRAC connection parameters (IP, credentials, etc.) as environment variables.
2.  **MQTT Parameters**: Provide MQTT broker details (host, user, password, etc.) for data publishing.
3.  **Data Points**: Define the data to be retrieved from iDRAC by setting `IDRAC_` prefixed environment variables.

## Usage

-   Set environment variables for iDRAC and MQTT parameters.
-   Define `IDRAC_` prefixed variables for each data point you wish to monitor.
-   Run the script to begin data extraction and publishing.
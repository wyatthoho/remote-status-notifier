# remote-status-notifier

A robust Python-based background utility that monitors 
Remote Desktop (RDP) user activity and synchronizes status 
changes to a Slack channel in real-time.

## Features

- **Real-time Monitoring**: 
  Detects when users connect or disconnect from the workstation.
- **Slack Integration**: 
  Automated status notifications sent via Slack API.
- **System Tray Integration**: 
  Runs quietly in the background with a convenient system tray icon.

## Requirements

- Python 3.12+
- Slack API token with access to the target Slack workspace
- Access to the workstation to monitor user sessions

## Running the Project

Create a `.env` file in the root directory and define the following variables:
```
COMPUTERNAME=YourWorkstationName
SLACK_TOKEN=xoxb-your-slack-token
SLACK_CHANNEL_IDX=your-channel-id-or-index
```

To run the project, use the following command:
```bash
.\run.bat
```

This script will:

- Automatically install any required dependencies (if needed)
- Activate the Python virtual environment
- Start the remote-status-notifier

This ensures you have everything set up and running with a single command.

## License

This project is licensed under the MIT License. See the 
`LICENSE` file for details.

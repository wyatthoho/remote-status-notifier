# remote-status-notifier

## Features

A Python script to monitor remote desktop user activity 
on a workstation and notify a specified Slack channel 
about status changes.

## Requirements

- Python 3.12 or higher
- Slack API token with access to the target Slack workspace
- Access to the workstation to monitor user sessions

See the `requirements.txt` file for the required Python
packages.

## License

This project is licensed under the MIT License. See the 
`LICENSE` file for details.

## Running the Project
First, configure the required system environment variables:

- `SLACK_TOKEN`: The Slack API token.
- `SLACK_CHANNEL_IDX`: The index of the Slack channel.

To run the project, use the following command:
```bash
.\run_in_venv.ps1
```

This script will:

- Automatically install any required dependencies (if needed)
- Activate the Python virtual environment
- Start the remote-status-notifier

This ensures you have everything set up and running with a single command.

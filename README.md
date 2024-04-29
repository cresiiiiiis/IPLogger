# Qydic-IPLogger

IPLogger is a free and open-source tool that helps you gather information about a target's system, including its private and public IP addresses, location, system information, and installed applications.

## Features

- Retrieves private and public IP addresses
- Determines the location based on the public IP address
- Gathers system information such as OS details, RAM, storage, and installed applications
- Sends collected information to a Discord webhook

## Usage

1. Clone this repository:

    ```bash
    git clone https://github.com/your-username/IPLogger.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the script:

    ```bash
    python a.py
    ```

4. The collected information will be sent to a Discord webhook.

## Dependencies

- requests
- psutil
- pyinstaller (for creating an executable)

## How to Contribute

Contributions are welcome! Here's how you can contribute to this project:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

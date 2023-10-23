# Health App

Health App is a mobile app designed to help elderly individuals manage their health. The app tracks vital signs, reminds users to take medication, and help chat with existing healthcare expert or other elders. The app is user-friendly and secure, ensuring the privacy of user data.

## Background Information

Similar solutions that have been identified include existing health management apps that track vital signs, remind users to take medication, and schedule appointments. These solutions can be leveraged by incorporating some of the best practices and features into the design of the app. The development of the app requires expertise in mobile app development, healthcare technology, and user experience design. On the team, there are experienced developers who have expertise in these fields and can contribute to the successful delivery of the project.

Some of the challenges that will be faced during the project include ensuring that the app is user-friendly and accessible to the elderly population, and that it integrates seamlessly with existing healthcare systems and devices. Additionally, ensuring the security and privacy of user data will be a crucial challenge. The technical hurdle that must be managed is the integration of various health tracking devices and systems with the app, ensuring that the app provides accurate and reliable health data to users. This requires expertise in device integration and data management.

## Features

- Vital signs tracking: The app tracks vital signs such as blood pressure, heart rate, and blood sugar levels.
- Appointment scheduling: Users can schedule appointments with healthcare providers directly from the app.
- Explore: Users can see other users' posts.
- Chat system: Users can chat with existing health experts or other users, providing accurate and reliable health data to users.
- User-friendly design: The app is designed to be easy to use and accessible to elderly individuals.
- Secure data storage: User data is stored securely, ensuring the privacy of user information.

## Run

Please ensure your Python3 version is >= 3.9.

To install the Health App, follow these steps:

1. Install SQLite and curl:  `sudo apt-get install sqlite3 curl`

2. Create virtual environment `python3 -m venv env`

3. Every time you open the directory, you must activate env:  `source env/bin/activate`

4. Download requirements:  `pip install -r requirements.txt`

5. Create app:  `pip install -e .`

6. Make executable:  `chmod +x ./bin/healthdb ./bin/healthtest ./bin/healthrun`

7. Reset database:  `./bin/healthdb reset`

8. Run:  `./bin/healthrun`

9. In Chrome, enter `localhost:8000`

   Default users: `awdeorio`, `jflinn`, `michjc`, `jag`. Passwords are all `password`.

## Contributing

If you would like to contribute to the Health App project, please submit a pull request. We welcome contributions from developers, software professionals, and user experience designers.

## License

The Health App is licensed under the MIT License. See LICENSE for more information.

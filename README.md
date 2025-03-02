# Django Blog

A fully functional blogging platform built with Django and Django Rest Framework (DRF), featuring a custom authentication system.

## Features

- **CRUD operations for posts**: Create, read, update, and delete blog posts.
- **User post management**:
  - Only active and staff users can create posts
  - Users can edit and delete their own posts
- **Custom authentication system**:
  - Login via email and password
  - Registration via phone number
  - Google authentication
  - Fully customized login & signup flow
- **Dockerized environment** for seamless deployment.

## Installation & Setup

### Prerequisites
Ensure you have the following installed:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setup Instructions

1. **Clone the repository**
   ```sh
   git clone https://github.com/erfanrazavi1/django-blog.git
   cd django-blog
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Build the Docker containers**
   ```sh
   docker-compose build
   ```

4. **Run the application**
   ```sh
   docker-compose up
   ```

The application will now be running, and you can access it at `http://localhost:8000/`.

## Future Enhancements
This project is continuously evolving, and many more features will be added in the future. Stay tuned! 🚀

## Contributing
Feel free to fork this repository and submit pull requests with improvements or bug fixes.

## License
This project is licensed under the MIT License.


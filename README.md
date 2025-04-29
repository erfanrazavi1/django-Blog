# 📝 Django Blog

A fully featured blog platform built with **Django** and **Django Rest Framework (DRF)**, supporting API-based interactions, background tasks, and modern development practices.

---

## 🚀 Features

### 📌 Post Management via API
- Full **CRUD operations** for blog posts using **Class-Based Views (CBVs)**
- Only **active** and **staff** users can create posts
- Users can **edit** and **delete** only their own posts
- All post interactions are **API-driven**

### 🔐 Authentication & Authorization
- Custom authentication:
  - Login with **email**
  - Registration via **phone number**
  - **Google authentication** support
- **JWT authentication** (`djangorestframework-simplejwt`)
- **Token authentication** supported
- Custom login and signup flow

### 🛢️ Database & Caching
- Uses **PostgreSQL** as the database
- **Redis** for caching and task queues

### 🛠️ Background Task Processing
- **Celery** integrated with **Redis** for background jobs

### 🧪 Testing & Load Testing
- Main test framework: **pytest**
- Support for `unittest`
- **Locust** for load testing
- **Faker** for generating fake data

### 🧹 Code Quality & Formatting
- **Black** and **Flake8** for code formatting and linting

### ⚙️ CI/CD
- Continuous Integration with **GitHub Actions**

### 📦 Deployment
- Fully **Dockerized**
  - Separate `docker-compose` files for **development** and **production**
- Production setup uses:
  - **Gunicorn** as the WSGI server
  - **Nginx** as the reverse proxy
  - Separate **staging** configuration supported

---

## ⚙️ Installation & Setup

### Prerequisites

Ensure the following are installed:
- [Docker](https://www.docker.com/get-started) (version 20.10 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 1.29 or higher)
- [Git](https://git-scm.com/downloads)

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/erfanrazavi1/django-blog.git
   cd django-blog
   ```


2. **Build and run Docker containers**

   ```bash
   docker-compose -f docker-compose.stage.yml up --build
   ```

   

3. **Apply database migrations**

   ```bash
   docker compose -f docker-compose-stage.yml sh -c "python manage.py migrate"
   ```

4. **Create super user**
  ```bash
  docker compose -f docker-compose-stage.yml sh -c "python manage.py createsuperuser" 
  ```
  
5. **Access the application**

   Open `http://localhost`.

---

## 🌱 Future Enhancements

This project is actively maintained, with planned features including:
- Enhanced user profiles
- Commenting system
- Advanced search functionality
- Integration with external APIs

Stay tuned for updates! 🚀

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository, open issues, or submit pull requests for improvements and bug fixes. Please follow the [contributing guidelines](CONTRIBUTING.md).

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

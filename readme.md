# Murder Mystery Solver Web Application

## Project Overview
Murder Mystery Solver is a Django-based web application designed to engage users in solving fictional murder cases by analyzing evidence, interviewing suspects, and reviewing investigator reports. The platform features user authentication, interactive case exploration, and admin-managed content.

## System Architecture

### Overall Architecture
The system follows a standard Django MVT (Model-View-Template) architecture:

- **Models**: Define the data structure for murders, suspects, investigators, and interviews
- **Views**: Handle request processing and business logic
- **Templates**: Render the UI for users
- **URLs**: Map URL patterns to appropriate views

### Components
1. **Core Application (main app)**
   - Handles murder cases, suspects, investigators, and interviews
   - Manages user accounts and authentication
   - Provides the main interface for investigating cases

2. **Chat System (chat app)**
   - Real-time support chat functionality
   - User-to-admin communication
   - Admin dashboard for message management

3. **Authentication System**
   - User registration with email verification
   - Password reset functionality
   - User profile management

4. **Admin Interface**
   - Content management for cases, suspects, and interviews
   - Dynamic relationship management between entities
   - Support chat monitoring and response

### Deployment Architecture
The application is designed for deployment on Azure with the following components:
- Django web application hosted on Azure App Service
- PostgreSQL database for production
- Azure Blob Storage for media files
- SQLite for local development

## Key Features

### User Features
1. **Case Exploration**
   - Browse available murder cases
   - View case details including dates, descriptions, and images
   - Access suspect profiles, investigator information, and interview transcripts

2. **Investigation Tools**
   - Review suspect profiles with detailed information
   - Analyze investigator backgrounds
   - Read interview transcripts with evidence images

3. **User Account Management**
   - Register with email verification
   - Update profile information
   - Password reset functionality

4. **Support System**
   - Real-time chat with administrators
   - Issue reporting and assistance

### Admin Features
1. **Content Management**
   - Create and manage murder cases, suspects, and investigators
   - Upload and manage media files
   - Create relationships between entities

2. **Support Dashboard**
   - View active chat conversations
   - Respond to user inquiries
   - Manage support chat history

3. **User Management**
   - Monitor user registrations
   - Verify email confirmations
   - Handle account issues

## Database Schema

### Main Models
1. **Murders**
   - `name`: Case name
   - `description`: Detailed case description
   - `short_description`: Brief summary
   - `image`: Case image
   - `date`: Date of occurrence

2. **Suspects**
   - `murders`: Foreign key to associated murder case
   - `name`: Suspect name
   - `description`: Background information
   - `age`: Suspect age
   - `image`: Suspect photo

3. **Investigators**
   - `murders`: Foreign key to associated murder case
   - `name`: Investigator name
   - `description`: Background and expertise
   - `age`: Investigator age
   - `image`: Investigator photo

4. **Interviews**
   - `murders`: Foreign key to associated murder case
   - `suspects`: Foreign key to interviewed suspect
   - `investigators`: Foreign key to conducting investigator
   - `content`: Interview transcript
   - `date`: Interview date/time
   - `image`: Optional evidence image

### Chat Models
1. **ChatRoom**
   - `user`: Foreign key to user
   - `murder_case`: Optional foreign key to relevant case
   - `subject`: Chat topic
   - `is_active`: Room status flag
   - `created_at`/`updated_at`: Timestamps

2. **ChatMessage**
   - `chat_room`: Foreign key to associated chat room
   - `sender`: Foreign key to message sender
   - `message`: Message content
   - `is_admin`: Flag for admin messages
   - `timestamp`: Message time
   - `is_read`: Read status flag

### User Models
- Extended Django User model with custom Profile model
- `UserProfile`: Contains email verification status and token

## API Endpoints

### Main Application
- `/`: Home page with case listing
- `/solve/<murder_id>/`: Detailed case view
- `/suspectsprofile/<murder_id>/`: Suspect profiles for a case
- `/investigatorsprofile/<murder_id>/`: Investigator profiles
- `/interviews/<murder_id>/`: Interview transcripts

### Authentication
- `/register/`: User registration
- `/login/`: User login
- `/logout/`: User logout
- `/activate/<uidb64>/<token>/`: Account activation
- `/password-reset/`: Password reset request
- `/password-reset/confirm/<uidb64>/<token>/`: Password reset confirmation

### AJAX Endpoints
- `/ajax/get-suspects/`: Get suspects for a murder case
- `/ajax/get-investigators/`: Get investigators for a murder case
- `/ajax/get-suspect-details/<suspect_id>/`: Get detailed suspect information
- `/ajax/get-investigator-details/<investigator_id>/`: Get investigator details
- `/ajax/get-interview-details/<interview_id>/`: Get interview transcript

### Chat System
- `/contact/`: User support chat interface
- `/support/chat/`: Admin chat dashboard
- `/ajax/get-new-messages/`: Polling for new messages
- `/ajax/send-message/`: Send a message
- `/ajax/clear-chat/`: Clear chat history
- `/support/clear-chat/`: Admin endpoint to clear chats

## Technology Stack

### Backend
- **Framework**: Django 5.2.1
- **Database**: 
  - Development: SQLite
  - Production: PostgreSQL on Azure
- **Storage**: 
  - Development: Local storage
  - Production: Azure Blob Storage
- **Authentication**: Django authentication system with custom extensions

### Frontend
- **HTML/CSS/JavaScript**: Core frontend technologies
- **CSS Framework**: Custom styling with responsive design
- **Template Engine**: Django template language
- **AJAX**: For dynamic content loading and chat functionality

### DevOps & Infrastructure
- **Version Control**: Git
- **Hosting**: Azure App Service
- **Database Hosting**: Azure PostgreSQL
- **Static/Media Storage**: Azure Blob Storage
- **Email Service**: SMTP integration

## Security Considerations

1. **Authentication Security**
   - Email verification for new accounts
   - Secure password reset flow
   - Admin access restrictions

2. **Data Protection**
   - CSRF protection on all forms
   - Secure handling of user data
   - Environment variable-based configuration

3. **Production Settings**
   - Debug mode disabled in production
   - HTTPS enforcement
   - Trusted origins for CSRF

4. **Middleware Security**
   - Admin access restriction middleware
   - Security middleware configurations

## Installation and Setup

### Prerequisites
- Python 3.8+
- pip
- Virtual environment tool (venv or conda)

### Local Development Setup
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd rev
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file with required environment variables**:
   ```
   DJANGO_SECRET_KEY=your_secret_key
   DJANGO_DEBUG=True
   EMAIL_HOST=your_smtp_host
   EMAIL_PORT=465
   EMAIL_HOST_USER=your_email
   EMAIL_HOST_PASSWORD=your_password
   DEFAULT_FROM_EMAIL=your_email
   ```

5. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - Web application: http://localhost:8000
   - Admin interface: http://localhost:8000/admin

### Production Deployment
1. Set up Azure resources:
   - App Service
   - PostgreSQL database
   - Blob Storage

2. Configure environment variables in Azure App Service:
   - Database connection string
   - Storage connection string
   - Email settings
   - Debug=False
   - Allowed hosts
   - CSRF trusted origins

3. Deploy code using Azure deployment options

## Environment Variables

### Required Variables
- `DJANGO_SECRET_KEY`: Secret key for Django app
- `DJANGO_DEBUG`: Boolean for debug mode
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DJANGO_CSRF_TRUSTED_ORIGINS`: Comma-separated list of trusted origins for CSRF

### Database (Production)
- `AZURE_POSTGRESQL_CONNECTIONSTRING`: Connection string for PostgreSQL

### Email Configuration
- `EMAIL_HOST`: SMTP server host
- `EMAIL_PORT`: SMTP server port
- `EMAIL_HOST_USER`: Email username/address
- `EMAIL_HOST_PASSWORD`: Email password
- `DEFAULT_FROM_EMAIL`: Default sender address

### Storage (Production)
- `AZURE_CONNECTION_STRING`: Azure storage connection string
- `AZURE_ACCOUNT_NAME`: Storage account name
- `AZURE_ACCOUNT_KEY`: Storage account key
- `AZURE_MEDIA_CONTAINER`: Container name for media files

## Directory Structure


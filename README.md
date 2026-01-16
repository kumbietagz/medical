# Medical Insurance Claims Management System

## Project Overview

This is a Django-based web application designed to streamline the management and validation of medical insurance claims between healthcare providers (doctors) and insurance processors. The system integrates machine learning models to assess claim legitimacy and predict approval confidence.

## Key Features

### 1. **User Management & Authentication**
- **Two Account Types:**
  - Doctors: Submit medical insurance claims
  - Claims Processors: Review and approve/reject claims
- Secure login/logout functionality
- User profiles with customizable display pictures
- Department and username tracking

### 2. **Claims Processing**
- **Claim Submission:** Doctors can submit claims with comprehensive patient information
- **Claim Fields:**
  - Patient demographics (age, gender)
  - Medical practice details
  - Claimed amount and tariff
  - Member information
  - Claim description
  - Approval status tracking
  - ML-generated confidence scores

- **Claim Management:**
  - View all claims
  - Update claim details
  - Delete claims
  - Search claims by description, doctor name, or approval status

### 3. **Machine Learning Integration**
- **Models Used:**
  - Extra Trees Classifier (`ml/extraTrees.pkl`)
  - Random Forest Classifier (`ml/randForest.pkl`)
- **Purpose:** Predict claim confidence levels to identify potentially fraudulent or high-risk claims
- **Training Data:** Final_Dataset.csv (available in `ml/` folder)
- Models are loaded at runtime via joblib

### 4. **Role-Based Dashboard**
- **Doctor Dashboard:**
  - View submitted claims
  - Submit new claims
  - Update claim status
- **Claims Processor Dashboard:**
  - Review all claims
  - Search and filter claims
  - Approve/reject claims
  - View ML confidence scores

### 5. **Search Functionality**
- Full-text search across claims
- Filter by:
  - Claim description
  - Doctor name
  - Approval status
  - Forest/Trees model results

## Project Structure

```
medical/                          # Main Django project
├── manage.py                     # Django management script
├── db.sqlite3                    # SQLite database
├── requirements.txt              # Python dependencies
│
├── medical/                      # Main app configuration
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Project URL routing
│   ├── wsgi.py                  # WSGI configuration
│   └── asgi.py                  # ASGI configuration
│
├── claim/                        # Claims app (core functionality)
│   ├── models.py                # Database models (Account, Claim)
│   ├── views.py                 # View logic and business logic
│   ├── urls.py                  # App-specific URL routing
│   ├── admin.py                 # Django admin configuration
│   ├── forms.py                 # Form definitions
│   ├── apps.py                  # App configuration
│   │
│   ├── migrations/              # Database migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_claim.py
│   │   ├── 0003_auto_20220329_0943.py
│   │   ├── 0004_auto_20220329_2149.py
│   │   ├── 0005_claim_member.py
│   │   ├── 0006_remove_account_password.py
│   │   └── 0007_auto_20220525_1103.py
│   │
│   ├── static/claim/            # Static files (CSS, JS, images)
│   │   ├── css/                 # Stylesheets
│   │   │   ├── bootstrap.css
│   │   │   ├── custom.css
│   │   │   ├── colors.css
│   │   │   ├── responsive.css
│   │   │   ├── dark.css
│   │   │   └── components/      # Component-specific styles
│   │   │
│   │   ├── js/                  # JavaScript files
│   │   │   ├── jquery.js
│   │   │   ├── chart.js
│   │   │   ├── functions.js
│   │   │   ├── plugins.js
│   │   │   └── plugins/         # jQuery plugins
│   │   │
│   │   ├── fonts/               # Font files
│   │   └── images/              # Image assets
│   │
│   └── templates/claim/         # HTML templates
│       ├── base.html            # Base template
│       ├── login.html           # Login page
│       ├── claimsHome.html      # Claims processor dashboard
│       ├── claimsDetail.html    # Claim details view
│       ├── allClaims.html       # List all claims
│       ├── myClaims.html        # Doctor's claims
│       ├── myClaimUpdate.html   # Update claim form
│       ├── doctorHome.html      # Doctor dashboard
│       ├── doctorsList.html     # List of doctors
│       ├── addDoctor.html       # Add doctor form
│       ├── doctorUpdate.html    # Update doctor form
│       ├── search.html          # Search results page
│       └── docSide.html         # Doctor sidebar
│
├── ml/                          # Machine Learning models
│   ├── Final_Dataset.csv        # Training dataset
│   ├── Untitled.ipynb           # Jupyter notebook (model development)
│   ├── extraTrees.pkl           # Trained Extra Trees model
│   └── randForest.pkl           # Trained Random Forest model
│
└── media/images/                # User-uploaded files (display pictures, etc.)
```

## Technology Stack

### Backend
- **Framework:** Django 4.0.3
- **Database:** SQLite3
- **Python Packages:**
  - asgiref==3.5.0
  - joblib==1.1.0 (for ML model loading)
  - Pillow==9.0.1 (image handling)
  - sqlparse==0.4.2

### Frontend
- **HTML5** with template inheritance
- **CSS3** (Bootstrap, custom stylesheets)
  - Responsive design
  - RTL (right-to-left) support for multi-language
  - Dark mode theme
- **JavaScript:** jQuery for interactivity
  - Chart.js for data visualization
  - Calendar functionality
  - Datepicker components

### Machine Learning
- **Models:** Scikit-learn (Extra Trees & Random Forest)
- **Serialization:** joblib

## Database Models

### Account Model
```python
- display_picture: Image (optional)
- user: ForeignKey to Django User
- accountType: 'Doctor' or 'Claims'
- name: User's full name
- department: Department name
- username: Username
```

### Claim Model
```python
- doctor: ForeignKey to Account (Doctor)
- claimed: Amount claimed (Integer)
- age: Patient age
- gender: Patient gender
- practice: Years of practice
- member: Member ID
- description: Claim description
- tariff: Tariff/cost
- approval: Approval status
- confidence: ML confidence score (0-1)
- trees: Extra Trees model result
- forest: Random Forest model result
- created_at: Timestamp
- updated_at: Timestamp
```

## Key Views & Endpoints

### Authentication
- `doctorLogin()` - Doctor login page
- `claimsLogin()` - Claims processor login page
- Logout functionality

### Doctor Views
- `doctor()` - Doctor dashboard (view submitted claims)
- Create claim
- Update claim
- View claim details

### Claims Processor Views
- `claimsHome()` - All claims dashboard
- `claimsDetail()` - View specific claim
- Approve/reject claims
- Search claims

### Search & Utilities
- `search()` - Full-text search across claims
- `doctorsList()` - View all doctors
- `addDoctor()` - Register new doctor

## Machine Learning Integration

The system uses two pre-trained classifiers to assess claim legitimacy:

1. **Extra Trees Classifier** - Provides high-variance estimate
2. **Random Forest Classifier** - Provides conservative estimate

Both models:
- Are loaded from pickle files at application startup
- Generate confidence scores stored in the claim record
- Help identify potentially fraudulent or high-risk claims
- Support claims processors in decision-making

## Setup & Installation

1. **Clone repository:**
   ```bash
   git clone <repository-url>
   cd medical
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (for admin panel):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Main site: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/

## Usage

### For Doctors
1. Log in with doctor credentials
2. Access doctor dashboard
3. Submit a new claim with patient information
4. View and update existing claims
5. Monitor claim approval status and ML confidence scores

### For Claims Processors
1. Log in with claims processor credentials
2. View all submitted claims
3. Review claim details and ML-generated confidence scores
4. Approve or reject claims
5. Search for specific claims using filters

## Future Enhancements

- [ ] Advanced visualization of claim trends
- [ ] Automated email notifications on claim status changes
- [ ] Batch claim processing
- [ ] Enhanced ML model with more sophisticated algorithms
- [ ] API endpoints for integration with other systems
- [ ] Mobile app for on-the-go claim submission
- [ ] Multi-language support (RTL CSS already in place)
- [ ] Real-time claim tracking with status updates

## Security Considerations

- User authentication required for all views
- Role-based access control (Doctor vs Claims)
- CSRF protection enabled
- SQL injection protection via ORM
- Image upload validation (via Pillow)

## Performance Notes

- ML models are loaded once at startup (not per-request)
- Database queries are optimized for dashboard views
- Static files are served efficiently
- Responsive CSS prevents rendering delays

## License

[Add appropriate license information]

## Contact & Support

[Add contact information]

---

**Last Updated:** January 16, 2026


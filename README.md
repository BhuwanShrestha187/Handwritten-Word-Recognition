# Handwritten OCR Application

A powerful web application that converts handwritten text to digital format using advanced OCR technology, with additional features like translation and text summarization.

## 🌟 Features

### Core Features
- **Handwritten Text Recognition**: Convert handwritten text from images to digital text
- **Multi-language Support**: Translate extracted text into various languages
- **Text Summarization**: Generate concise summaries of long texts
- **User Authentication**: Secure login and signup system
- **File Management**: Support for multiple file formats (PDF, DOCX, TXT)
- **History Tracking**: Keep track of all your OCR conversions
- **User Settings**: Customize your account preferences

### Technical Features
- **Cloud Integration**: Deployed on Google Cloud Platform
- **Database**: SQLite for user data and conversion history
- **Security**: Secure password handling and user authentication
- **Responsive Design**: Mobile-friendly interface
- **File Processing**: Support for multiple file uploads

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite
- **Authentication**: Flask-Login
- **Cloud Services**: Google Cloud Vision API
- **Translation**: Deep Translator
- **Text Processing**: Transformers (Hugging Face)

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap (for responsive design)

### APIs Used
- Google Cloud Vision API (OCR)
- LibreTranslate API (Translation)
- Custom Summarization API

## 📦 Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd Handwritten_OCR_V8
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
python init_db.py
```

## 🔧 Configuration

1. Set up Google Cloud Project:
   - Create a project in Google Cloud Console
   - Enable Vision API
   - Create service account and download credentials
   - Update `GOOGLE_CLOUD_PROJECT` in `.env`

2. Configure environment variables:
   - `SECRET_KEY`: Generate a secure key
   - `DATABASE_URL`: SQLite database path
   - `GOOGLE_CLOUD_PROJECT`: Your Google Cloud project ID

## 🚀 Deployment

The application is configured for deployment on Google Cloud Platform:

1. Install Google Cloud SDK
2. Authenticate:
```bash
gcloud auth login
```
3. Set project:
```bash
gcloud config set project handwritten-ocr-app
```
4. Deploy:
```bash
gcloud app deploy app.yaml
```

## 🎯 Usage

1. **User Registration**:
   - Sign up with email and password
   - Verify your account

2. **Text Extraction**:
   - Upload handwritten images
   - View extracted text
   - Edit if necessary

3. **Additional Features**:
   - Translate text to different languages
   - Generate summaries
   - Download in various formats
   - View conversion history

## 🎨 Interesting Implementation Details

### OCR Processing
- Implemented advanced image preprocessing for better text recognition
- Handles various handwriting styles and image qualities
- Supports multiple image formats

### Translation System
- Real-time translation using Deep Translator
- Supports multiple languages
- Maintains text formatting during translation

### Security Features
- Password hashing using bcrypt
- Session management with Flask-Login
- Secure file handling and validation

## 🚧 Challenges and Solutions

### Challenge 1: Image Quality
**Problem**: Poor quality images affecting OCR accuracy
**Solution**: Implemented image preprocessing pipeline
- Contrast enhancement
- Noise reduction
- Image normalization

### Challenge 2: Multi-language Support
**Problem**: Complex text formatting in different languages
**Solution**: 
- Implemented Unicode support
- Added language-specific text processing
- Created custom formatting handlers

### Challenge 3: Scalability
**Problem**: Performance issues with large files
**Solution**:
- Implemented file chunking
- Added background processing
- Optimized database queries

## 👥 Team

- **Bhuwan Shrestha**: Lead Developer
- **Alen Varghese**: UI/UX Designer
- **Shubh Soni**: Machine Learning Expert
- **Dev Patel**: Backend Engineer

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## 📞 Support

For support, email support@handwrittenocr.com or create an issue in the repository. 
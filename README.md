<div align="center">

# ✍️ Handwritten OCR Application ✍️

<img src="https://img.shields.io/badge/status-active-brightgreen" alt="Status" />
<img src="https://img.shields.io/badge/license-MIT-blue" alt="License" />
<img src="https://img.shields.io/badge/version-1.0-orange" alt="Version" />

```
   _    _                _                  _ _   _               ___   ____ ____
  | |  | |              | |                (_) | | |             / _ \ / ___|  _ \
  | |__| | __ _ _ __  __| |_      ___ __ ___| |_| |_ ___ _ __  | | | | |   | |_) |
  |  __  |/ _` | '_ \/ _` \ \ /\ / / '__/ _ \ __| __/ _ \ '_ \ | | | | |   |  _ <
  | |  | | (_| | | | | (_| |\ V  V /| | |  __/ |_| ||  __/ | | || |_| | |___| |_) |
  |_|  |_|\__,_|_| |_|\__,_| \_/\_/ |_|  \___|\__|\__\___|_| |_(_)___/ \____|____/
```

_A powerful web application that converts handwritten text to digital format using advanced OCR technology_

</div>

---

<div align="center">
  
📝 **Convert** • 🌐 **Translate** • 📊 **Summarize** • 📱 **Access Anywhere**
  
</div>

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#️-technology-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [Usage](#-usage)
- [Implementation Details](#-interesting-implementation-details)
- [Challenges and Solutions](#-challenges-and-solutions)
- [Team](#-team)
- [License](#-license)
- [Contributing](#-contributing)
- [Support](#-support)

---

## 🌟 Features

<details open>
<summary><b>Core Features</b></summary>
<br>

| Feature                             | Description                                          |
| ----------------------------------- | ---------------------------------------------------- |
| ✨ **Handwritten Text Recognition** | Convert handwritten text from images to digital text |
| 🌐 **Multi-language Support**       | Translate extracted text into various languages      |
| 📝 **Text Summarization**           | Generate concise summaries of long texts             |
| 🔐 **User Authentication**          | Secure login and signup system                       |
| 📁 **File Management**              | Support for multiple file formats (PDF, DOCX, TXT)   |
| 📊 **History Tracking**             | Keep track of all your OCR conversions               |
| ⚙️ **User Settings**                | Customize your account preferences                   |

</details>

<details>
<summary><b>Technical Features</b></summary>
<br>

| Feature                  | Description                                      |
| ------------------------ | ------------------------------------------------ |
| ☁️ **Cloud Integration** | Deployed on Google Cloud Platform                |
| 🗄️ **Database**          | SQLite for user data and conversion history      |
| 🔒 **Security**          | Secure password handling and user authentication |
| 📱 **Responsive Design** | Mobile-friendly interface                        |
| 📂 **File Processing**   | Support for multiple file uploads                |

</details>

---

## 🛠️ Technology Stack

<div align="center">

### 🔙 Backend

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

### �� Frontend

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

### 🔌 APIs Used

- Google Cloud Vision API (OCR)
- LibreTranslate API (Translation)
- Custom Summarization API

</div>

---

## 📦 Installation

<div align="center">
  
```
🚀 Get up and running in 5 simple steps 🚀
```

</div>

1️⃣ **Clone the repository:**

```bash
git clone [repository-url]
cd Handwritten_OCR_V8
```

2️⃣ **Create and activate virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3️⃣ **Install dependencies:**

```bash
pip install -r requirements.txt
```

4️⃣ **Set up environment variables:**

```bash
cp .env.example .env
# Edit .env with your configuration
```

5️⃣ **Initialize the database:**

```bash
python init_db.py
```

---

## 🔧 Configuration

<details>
<summary><b>Google Cloud Setup</b></summary>
<br>

1. Create a project in Google Cloud Console
2. Enable Vision API
3. Create service account and download credentials
4. Update `GOOGLE_CLOUD_PROJECT` in `.env`

</details>

<details>
<summary><b>Environment Variables</b></summary>
<br>

- `SECRET_KEY`: Generate a secure key
- `DATABASE_URL`: SQLite database path
- `GOOGLE_CLOUD_PROJECT`: Your Google Cloud project ID

</details>

---

## 🚀 Deployment

<div align="center">
  
```
☁️ Deploy to the cloud in 4 easy steps ☁️
```

</div>

1️⃣ **Install Google Cloud SDK**

2️⃣ **Authenticate:**

```bash
gcloud auth login
```

3️⃣ **Set project:**

```bash
gcloud config set project handwritten-ocr-app
```

4️⃣ **Deploy:**

```bash
gcloud app deploy app.yaml
```

---

## 🎯 Usage

<details open>
<summary><b>User Registration</b></summary>
<br>

- Sign up with email and password
- Verify your account

</details>

<details open>
<summary><b>Text Extraction</b></summary>
<br>

- Upload handwritten images
- View extracted text
- Edit if necessary

</details>

<details open>
<summary><b>Additional Features</b></summary>
<br>

- Translate text to different languages
- Generate summaries
- Download in various formats
- View conversion history

</details>

---

## 🎨 Interesting Implementation Details

<div align="center">
  
```
💡 Technical highlights of our application 💡
```

</div>

<details>
<summary><b>OCR Processing</b></summary>
<br>

- Implemented advanced image preprocessing for better text recognition
- Handles various handwriting styles and image qualities
- Supports multiple image formats

</details>

<details>
<summary><b>Translation System</b></summary>
<br>

- Real-time translation using Deep Translator
- Supports multiple languages
- Maintains text formatting during translation

</details>

<details>
<summary><b>Security Features</b></summary>
<br>

- Password hashing using bcrypt
- Session management with Flask-Login
- Secure file handling and validation

</details>

---

## 🚧 Challenges and Solutions

<details>
<summary><b>Challenge 1: Image Quality</b></summary>
<br>

**Problem**: Poor quality images affecting OCR accuracy

**Solution**: Implemented image preprocessing pipeline

- Contrast enhancement
- Noise reduction
- Image normalization

</details>

<details>
<summary><b>Challenge 2: Multi-language Support</b></summary>
<br>

**Problem**: Complex text formatting in different languages

**Solution**:

- Implemented Unicode support
- Added language-specific text processing
- Created custom formatting handlers

</details>

<details>
<summary><b>Challenge 3: Scalability</b></summary>
<br>

**Problem**: Performance issues with large files

**Solution**:

- Implemented file chunking
- Added background processing
- Optimized database queries

</details>

---

## 👥 Team

<div align="center">

|                         **Bhuwan Shrestha**                         |                    **Alen Varghese**                     |                        **Shubh Soni**                         |                          **Dev Patel**                           |
| :-----------------------------------------------------------------: | :------------------------------------------------------: | :-----------------------------------------------------------: | :--------------------------------------------------------------: |
|                           UI/UX Designer                            |                       Scrum Master                       |                         Product Owner                         |                        Backend Developer                         |
| ![Designer](https://img.shields.io/badge/UI/UX-Designer-blueviolet) | ![Scrum](https://img.shields.io/badge/Scrum-Master-blue) | ![Product](https://img.shields.io/badge/Product-Owner-orange) | ![Backend](https://img.shields.io/badge/Backend-Developer-green) |

</div>

---

## 📝 License

<div align="center">
  
This project is licensed under the MIT License - see the LICENSE file for details.

![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

</div>

---

## 🤝 Contributing

<div align="center">
  
```
🌟 We welcome contributions! 🌟
```

</div>

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

---

## 📞 Support

<div align="center">
  
Need help? Contact us!

📧 [handwrittenocr448@gmail.com](mailto:handwrittenocr448@gmail.com)

or

🐛 [Create an issue](https://github.com/yourusername/handwritten-ocr/issues)

</div>

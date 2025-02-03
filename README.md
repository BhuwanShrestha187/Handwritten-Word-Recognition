# Handwritten Text Recognition Web Application

This project implements a web-based Handwritten Text Recognition system using TensorFlow, Flask, and the IAM Words dataset.

## Project Overview
- Convert handwritten text images to digital text
- Web interface for easy image upload and processing
- Real-time text recognition results

## Prerequisites
Before running this project, make sure you have:
- Python 3.8 or higher
- Git
- pip (Python package installer)
- 8GB RAM or higher recommended
- Internet connection for downloading datasets

## Required Dependencies
```bash
flask==2.0.1
numpy==1.21.0
opencv-python==4.5.3.56
pillow==8.3.1
tensorflow==2.7.0
mltu==1.0.0
```

## Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/BhuwanShrestha187/Handwritten-Letter-Recognition.git
cd Handwritten-Word-Recognition
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download IAM Dataset:
- Visit [IAM Dataset Website](https://fki.tic.heia-fr.ch/databases/iam-handwriting-database)
- Download 'words.tgz'
- Extract to 'data/raw' directory

## Project Structure
```
project/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   └── models.py
├── data/
│   ├── raw/            # Original IAM dataset
│   └── processed/      # Processed images
├── models/
│   └── configurations/ # Model config files
├── static/
│   ├── css/
│   └── js/
├── templates/
├── utils/
│   ├── preprocessing.py
│   └── data_loader.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Running the Application

1. Set up Flask environment:
```bash
# Windows
set FLASK_APP=app.py
set FLASK_DEBUG=1

# Mac/Linux
export FLASK_APP=app.py
export FLASK_DEBUG=1
```

2. Start the application:
```bash
flask run
```

3. Access the web interface:
- Open browser and go to: http://127.0.0.1:5000/

## Development Workflow

1. Create new branch for features:
```bash
git checkout -b feature-name
```

2. Make changes and commit:
```bash
git add .
git commit -m "Description of changes"
```

3. Push changes to your branch:
```bash
git push origin feature-name
```

## Testing
- Unit tests are in the `tests/` directory
- Run tests using: `python -m pytest`

## Common Issues and Solutions

1. Package Installation Errors:
   - Ensure virtual environment is activated
   - Try: `pip install --upgrade pip`
   - Install packages individually if needed

2. Dataset Issues:
   - Verify dataset is extracted correctly
   - Check file permissions
   - Ensure proper directory structure

3. Memory Issues:
   - Close unnecessary applications
   - Reduce batch size in configuration
   - Check available system resources

## Contributing
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## Team Members
- Product Owner: Shubh Soni
- Scrum Master: Alen Varghese
- Development Lead: Bhuwan Shrestha
- Testing Lead: Dev Patel

## Project Status
Currently in development phase:
- Environment setup complete
- Basic preprocessing pipeline implemented
- Working on model training pipeline
- Implementing web interface features

## License
This project is licensed under the MIT License - see the LICENSE file for details.

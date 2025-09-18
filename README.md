# FreeScraping - Freelance Market Analysis Tool

A Python GUI application for tracking and analyzing freelance job market trends from Free-Work.com.

## 🚀 Features

- **Real-time Job Market Scraping**: Automatically collects freelance job listings from Free-Work.com
- **Interactive GUI**: User-friendly tkinter interface for easy keyword searches
- **Weekly Trend Analysis**: Groups job postings by week to identify market patterns
- **Data Visualization**: Interactive matplotlib charts with hover functionality
- **Market Intelligence**: Track demand for specific skills and technologies

## 🛠️ Tech Stack

- **Backend**: Python 3.x
- **Web Scraping**: requests, BeautifulSoup4
- **GUI Framework**: tkinter (built-in Python)
- **Data Analysis**: pandas
- **Visualization**: matplotlib, mplcursors
- **Database**: SQLite (annonces.db)

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/Valerian5788/freeScraping.git
cd freeScraping
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python scraping.py
```

## 🎯 Usage

1. **Search Keywords**: Enter a technology or skill keyword (e.g., "Python", "React", "Data Science")
2. **Launch Scraping**: Click "Lancer le scraping" to collect job data
3. **View Results**: See the total number of matching job listings
4. **Analyze Trends**: Click "Afficher le graphique" to visualize weekly trends
5. **Interactive Charts**: Hover over data points to see detailed information

## 📊 Key Capabilities

- **Market Research**: Identify trending technologies and skills
- **Competitive Analysis**: Compare demand across different domains
- **Career Planning**: Make data-driven decisions about skill development
- **Freelance Strategy**: Optimize your service offerings based on market demand

## 🔧 Technical Implementation

### Web Scraping Engine
- Handles pagination automatically
- Parses job posting dates and metadata
- Implements respectful scraping practices
- Error handling for network issues

### Data Processing
- Weekly aggregation of job postings
- Efficient data storage and retrieval
- Time-series analysis preparation

### Visualization
- Interactive matplotlib charts
- Date-based x-axis formatting
- Hover tooltips for detailed information
- Clean, professional styling

## 📈 Project Value

This project demonstrates:
- **Web Scraping Expertise**: Real-world data extraction from dynamic websites
- **GUI Development**: Cross-platform desktop application creation
- **Data Analysis**: Time-series analysis and visualization
- **Market Intelligence**: Business problem-solving through automation
- **Python Proficiency**: Object-oriented programming and library integration

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements.

## 📄 License

This project is for educational and personal use. Please respect website terms of service when scraping.

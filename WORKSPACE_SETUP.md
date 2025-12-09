# Workspace Configuration - Mini Project 3

## 📁 Project Structure

```
mini-project-3-mark-barlow/
├── assets/              # Original project assets (data files, images)
│   ├── map.png
│   ├── ride_hailing.xlsx
│   └── plates/          # License plate images
├── src/                 # Source code directory
├── data/                # Data processing directories
│   ├── raw/            # Original, unprocessed data
│   ├── processed/      # Cleaned and transformed data
│   └── output/         # Final results and exports
├── tests/               # Test files
├── docs/                # Documentation
├── config/              # Configuration files
├── scripts/             # Utility scripts
├── .vscode/             # VS Code workspace settings
├── .gitignore           # Git ignore rules
├── requirements.txt     # Python dependencies
├── package.json         # Node.js dependencies (if using JS/TS)
└── setup.sh             # Workspace setup script
```

## 🚀 Quick Start

### Option 1: Use the Setup Script
```bash
./setup.sh
```

### Option 2: Manual Setup

#### Python Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install dependencies (uncomment what you need in requirements.txt first)
pip install -r requirements.txt
```

#### Node.js Setup (if using JavaScript/TypeScript)
```bash
npm install
```

## 🔧 Configuration

1. **Copy the example config:**
   ```bash
   cp config/config.example.json config/config.json
   ```

2. **Edit `config/config.json`** with your project-specific settings

## 📝 Next Steps

1. **Choose your tech stack:**
   - Python (data analysis, ML, web with Flask/FastAPI)
   - Node.js/TypeScript (web applications, APIs)
   - Or both!

2. **Copy from Mini Project 2 (if desired):**
   - Located at: `../Downloads/MiniProject2_MarkBarlow/`
   - Copy relevant code to `src/` directory

3. **Start coding:**
   - Main entry point: `src/main.py` or `src/index.js`
   - Add your logic in the `src/` directory
   - Use `data/` for data processing workflows

## 🛠️ Development Tools

### VS Code Extensions (Recommended)
The workspace includes recommended extensions in `.vscode/extensions.json`:
- Python extension
- ESLint (for JavaScript/TypeScript)
- Prettier (code formatting)

### Python Development
- Virtual environment: `venv/`
- Linting: flake8 (configured in VS Code)
- Formatting: Black (configured in VS Code)

## 📊 Data Files

Your project includes:
- `assets/ride_hailing.xlsx` - Excel data file
- `assets/map.png` - Map image
- `assets/plates/` - License plate images

## 🔐 Environment Variables

Create a `.env` file in the root directory for sensitive configuration:
```bash
# .env
API_KEY=your_api_key_here
DATABASE_URL=your_database_url
```

The `.env` file is already in `.gitignore` for security.

## ✅ Workspace Configuration Complete!

You're ready to start developing. Choose your tech stack and begin coding in the `src/` directory.

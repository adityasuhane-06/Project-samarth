# Contributing to Project Samarth

Thank you for your interest in contributing to Project Samarth! This document provides guidelines and instructions for contributing.

## 🎯 Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit bug fixes
- ✨ Add new features
- 🧪 Write tests
- 🎨 Improve UI/UX

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/project-samarth.git
cd project-samarth
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your credentials
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

## 📝 Development Guidelines

### Code Style

- Follow **PEP 8** style guide
- Use **type hints** for function parameters and return values
- Add **docstrings** for all functions and classes
- Keep functions **short and focused** (single responsibility)
- Use **meaningful variable names**

Example:
```python
from typing import Optional, Dict, Any

def fetch_crop_data(
    state: str,
    crop: str,
    year: int
) -> Optional[Dict[str, Any]]:
    """
    Fetch crop production data for a specific state, crop, and year.
    
    Args:
        state: Name of the Indian state
        crop: Name of the crop
        year: Year for which data is needed
        
    Returns:
        Dictionary containing production data or None if not found
    """
    # Implementation here
    pass
```

### Project Structure

When adding new features, follow the modular structure:

```
src/
├── config/         # Configuration and settings
├── models/         # Pydantic models
├── database/       # Database operations
├── services/       # Business logic
│   ├── ai_models.py           # AI model interactions
│   ├── data_integration.py    # External API integration
│   └── query_engine.py        # Query processing
└── api/            # API endpoints
```

### Adding a New Data Source

1. Add integration method in `services/data_integration.py`:
```python
def fetch_new_data_source(self, params: Dict) -> pd.DataFrame:
    """Fetch data from new source."""
    pass
```

2. Add query method in `services/query_engine.py`:
```python
def query_new_data_source(self, params: Dict) -> Dict[str, Any]:
    """Query the new data source."""
    pass
```

3. Update routing logic in `services/ai_models.py` if needed

4. Add cache TTL in `config/settings.py`:
```python
CACHE_TTL: Dict[str, int] = {
    "new_data_source": 90,  # days
}
```

### Adding a New API Endpoint

1. Add route in `api/routes.py`:
```python
@router.get("/api/new-endpoint")
async def new_endpoint():
    """Handle new endpoint."""
    pass
```

2. Add Pydantic models in `models/api_models.py` if needed:
```python
class NewRequest(BaseModel):
    field: str
```

### Testing

Before submitting a PR:

```bash
# Run manual tests
python test/test_system.py

# Test imports
cd src
python -c "from config import settings; from models import QueryRequest; from services import QueryRouter; print('✅ All imports OK')"

# Test API endpoints
curl http://localhost:8000/api/health
```

### Documentation

- Update relevant documentation in `docs/` folder
- Add docstrings to all new functions/classes
- Update `README.md` if adding major features
- Add examples for new functionality

## 🔍 Pull Request Process

### 1. Ensure Quality

- ✅ Code follows PEP 8 style guide
- ✅ All functions have docstrings
- ✅ Type hints are used
- ✅ Tests pass
- ✅ Documentation is updated
- ✅ No unnecessary files committed

### 2. Commit Messages

Use clear, descriptive commit messages:

```bash
# Good
git commit -m "Add APEDA export data integration"
git commit -m "Fix cache TTL calculation for rainfall data"
git commit -m "Update documentation for two-model architecture"

# Bad
git commit -m "update"
git commit -m "fix bug"
git commit -m "changes"
```

Follow this format:
```
<type>: <short description>

<detailed description if needed>

<issue reference if applicable>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

### 3. Create Pull Request

1. Push your branch:
```bash
git push origin feature/your-feature-name
```

2. Go to GitHub and create a Pull Request

3. Fill in the PR template:
   - Description of changes
   - Related issues
   - Testing performed
   - Screenshots (if UI changes)

### 4. Code Review

- Respond to feedback promptly
- Make requested changes
- Keep the PR focused and small
- Be open to suggestions

## 🐛 Reporting Bugs

### Before Reporting

- Check if the bug has already been reported
- Test with the latest version
- Gather reproduction steps

### Bug Report Template

```markdown
**Description**
A clear description of the bug.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g., Windows 10]
- Python Version: [e.g., 3.9]
- Project Version: [e.g., 1.0.0]

**Logs**
```
Paste relevant logs here
```

**Screenshots**
If applicable, add screenshots.
```

## 💡 Suggesting Features

### Feature Request Template

```markdown
**Feature Description**
A clear description of the feature.

**Use Case**
Why is this feature needed? What problem does it solve?

**Proposed Solution**
How would you implement this feature?

**Alternatives Considered**
Other solutions you've considered.

**Additional Context**
Any other context or screenshots.
```

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)
- [Google Gemini AI](https://ai.google.dev/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## 🎖️ Recognition

Contributors will be recognized in:
- README.md (Contributors section)
- Release notes
- Project documentation

## 📞 Questions?

- Open a GitHub Discussion
- Check existing documentation in `docs/`
- Review closed issues for similar questions

## 📋 Checklist for Contributors

Before submitting a PR, ensure:

- [ ] Code follows PEP 8
- [ ] All functions have docstrings
- [ ] Type hints are used
- [ ] Tests pass
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main
- [ ] No merge conflicts
- [ ] `.env` file not committed
- [ ] No unnecessary files in commit

---

Thank you for contributing to Project Samarth! Your contributions help make agricultural data more accessible. 🌾

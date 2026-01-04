# agent.md - AI Agent Development Guide for json2toon

> **Purpose**: This document provides comprehensive technical specifications, architecture decisions, and implementation guidance for AI agents to understand and build the json2toon library.

---

## 1. Project Overview

### 1.1 What is json2toon?

`json2toon` is a Python library that converts JSON structures into **TOON (Token-Oriented Object Notation)**, a more token-efficient format optimized for LLM interactions. The library helps reduce token costs when passing structured data to language models while maintaining readability and structure.

### 1.2 Key Objectives

- **Token Efficiency**: Reduce token count compared to verbose JSON
- **Structure Preservation**: Keep data relationships explicit
- **LLM Integration**: Provide prompt helpers with code fences and instructions
- **Bidirectional Conversion**: Support JSON → TOON and TOON → JSON
- **Smart Analysis**: Detect and optimize primitive arrays, uniform object arrays, and nested structures

### 1.3 Target Use Cases

- Passing large datasets to LLMs with reduced token costs
- Creating LLM-friendly data representations for API responses
- Compressing configuration files for model context
- Generating structured prompts with embedded data

---

## 2. TOON Format Specification

### 2.1 Core Principles

TOON optimizes JSON by:
1. Using **tabular format** for uniform arrays of objects
2. **Compressing repeated keys** in object collections
3. Using **shorthand notation** for primitive arrays
4. **Preserving nesting** where beneficial
5. **Maintaining type information** implicitly

### 2.2 Conversion Rules

#### 2.2.1 Primitive Values

```
JSON:                    TOON:
{"name": "Alice"}   →   name: Alice
{"age": 30}         →   age: 30
{"active": true}    →   active: true
{"data": null}      →   data: null
```

#### 2.2.2 Primitive Arrays

```
JSON:                           TOON:
{"numbers": [1, 2, 3, 4]}  →   numbers: [1, 2, 3, 4]
{"tags": ["a", "b", "c"]}  →   tags: [a, b, c]
```

#### 2.2.3 Uniform Object Arrays (Tabular Format)

This is where TOON shines - converting repeated object structures into tables:

```
JSON:
{
  "users": [
    {"id": 1, "name": "Alice", "role": "admin"},
    {"id": 2, "name": "Bob", "role": "user"},
    {"id": 3, "name": "Charlie", "role": "user"}
  ]
}

TOON:
users:
| id | name    | role  |
|----|---------|-------|
| 1  | Alice   | admin |
| 2  | Bob     | user  |
| 3  | Charlie | user  |
```

#### 2.2.4 Nested Structures

```
JSON:
{
  "user": {
    "name": "Alice",
    "contact": {
      "email": "alice@example.com",
      "phone": "555-0100"
    }
  }
}

TOON:
user:
  name: Alice
  contact:
    email: alice@example.com
    phone: 555-0100
```

#### 2.2.5 Mixed Arrays (Non-uniform)

For non-uniform arrays, preserve JSON-like structure:

```
JSON:
{"mixed": [1, "text", {"key": "value"}]}

TOON:
mixed: [1, text, {key: value}]
```

### 2.3 Edge Cases

- **Empty arrays**: `items: []`
- **Empty objects**: `config: {}`
- **Null values**: `field: null`
- **Special characters in strings**: Escape or quote when necessary
- **Very long strings**: Consider truncation markers with configuration

---

## 3. Architecture & Module Design

### 3.1 Module Dependency Graph

```
exceptions.py (base)
       ↓
config.py → analyzer.py → encoder.py → prompt.py
       ↓           ↓            ↓
       ↓           ↓       decoder.py
       ↓           ↓            ↓
       └─────→ metrics.py ←────┘
                    ↓
                 cli.py
```

### 3.2 Module Specifications

#### 3.2.1 `exceptions.py`

**Purpose**: Define custom exceptions for error handling

**Classes**:
- `Json2ToonError`: Base exception class
- `EncodingError`: Raised during JSON → TOON conversion failures
- `DecodingError`: Raised during TOON → JSON conversion failures
- `AnalysisError`: Raised when structure analysis fails
- `ConfigurationError`: Raised for invalid configuration

**Design Pattern**: Inherit from built-in `Exception`, add context information

---

#### 3.2.2 `config.py`

**Purpose**: Manage configuration settings for conversion behavior

**Classes**:
```python
@dataclass
class ToonConfig:
    # Table formatting
    table_separator: str = "|"
    header_separator: str = "-"
    
    # Array handling
    max_inline_array_length: int = 10
    compress_primitive_arrays: bool = True
    
    # String handling
    max_string_length: Optional[int] = None
    quote_strings: bool = False
    
    # Nesting
    indent_size: int = 2
    max_nesting_depth: int = 10
    
    # Analysis
    uniformity_threshold: float = 0.8  # 80% of objects must match structure
    min_table_rows: int = 2  # Minimum rows to use table format
```

**Functions**:
- `load_config(path: str) -> ToonConfig`: Load from JSON/YAML
- `save_config(config: ToonConfig, path: str)`: Save configuration
- `get_default_config() -> ToonConfig`: Return default settings

---

#### 3.2.3 `analyzer.py`

**Purpose**: Analyze JSON structure to determine optimal TOON representation

**Key Functions**:

```python
def analyze_structure(data: Any, config: ToonConfig) -> StructureInfo:
    """
    Analyze data structure and return metadata for encoding decisions.
    
    Returns StructureInfo with:
    - type: 'primitive' | 'array' | 'object' | 'nested'
    - is_uniform: bool (for arrays)
    - keys: List[str] (for uniform object arrays)
    - depth: int
    - estimated_tokens: int
    """

def is_uniform_array(arr: List[dict], threshold: float) -> Tuple[bool, List[str]]:
    """
    Check if array of objects has uniform structure.
    Returns (is_uniform, common_keys)
    """

def estimate_json_tokens(data: Any) -> int:
    """Estimate token count for JSON representation"""

def estimate_toon_tokens(data: Any, structure: StructureInfo) -> int:
    """Estimate token count for TOON representation"""

def should_use_table_format(arr: List[dict], config: ToonConfig) -> bool:
    """Decide if array should use table format"""
```

**Data Classes**:
```python
@dataclass
class StructureInfo:
    data_type: str
    is_uniform: bool
    keys: List[str]
    depth: int
    estimated_json_tokens: int
    estimated_toon_tokens: int
    savings_percent: float
```

---

#### 3.2.4 `encoder.py`

**Purpose**: Convert JSON to TOON format

**Main Class**:

```python
class ToonEncoder:
    def __init__(self, config: ToonConfig = None):
        self.config = config or get_default_config()
        self.analyzer = Analyzer(self.config)
    
    def encode(self, data: Any) -> str:
        """Convert JSON data to TOON string"""
    
    def encode_to_file(self, data: Any, filepath: str):
        """Encode and write to file"""
```

**Internal Methods**:
```python
def _encode_primitive(self, value: Any) -> str
def _encode_array(self, arr: List, indent: int = 0) -> str
def _encode_object(self, obj: dict, indent: int = 0) -> str
def _encode_table(self, arr: List[dict], keys: List[str], indent: int = 0) -> str
def _format_table_row(self, obj: dict, keys: List[str]) -> str
def _format_value(self, value: Any) -> str
```

**Algorithm Flow**:
1. Analyze structure with `analyzer`
2. Dispatch to appropriate encoding method based on type
3. Apply formatting rules from config
4. Handle nesting with indentation
5. Return TOON string

---

#### 3.2.5 `decoder.py`

**Purpose**: Convert TOON back to JSON

**Main Class**:

```python
class ToonDecoder:
    def __init__(self, config: ToonConfig = None):
        self.config = config or get_default_config()
    
    def decode(self, toon_str: str) -> Any:
        """Convert TOON string to JSON data"""
    
    def decode_from_file(self, filepath: str) -> Any:
        """Read TOON file and decode"""
```

**Internal Methods**:
```python
def _parse_line(self, line: str, indent_level: int) -> Tuple[str, Any]
def _parse_table(self, lines: List[str]) -> List[dict]
def _parse_array(self, content: str) -> List
def _parse_value(self, value_str: str) -> Any
def _detect_structure_type(self, lines: List[str]) -> str
```

**Algorithm Flow**:
1. Tokenize TOON string by lines
2. Detect structure type (table, nested object, array, primitive)
3. Parse recursively based on indentation
4. Reconstruct JSON structure
5. Return Python dict/list/primitive

**Note**: Initial implementation can support a subset of TOON features, expanding over time.

---

#### 3.2.6 `prompt.py`

**Purpose**: Wrap TOON data in LLM-friendly prompts

**Functions**:

```python
def create_llm_prompt(
    data: Any,
    instruction: str = "",
    format_as_toon: bool = True,
    add_code_fence: bool = True,
    fence_language: str = "toon"
) -> str:
    """
    Create a complete LLM prompt with embedded data.
    
    Example output:
    '''
    {instruction}
    
    ```toon
    {toon_encoded_data}
    ```
    '''
    """

def create_response_template(
    expected_fields: List[str],
    use_table: bool = False
) -> str:
    """Generate a response template for LLM to fill in TOON format"""

def wrap_in_code_fence(content: str, language: str = "toon") -> str:
    """Wrap content in markdown code fence"""

def add_system_prompt(toon_data: str, system_msg: str) -> dict:
    """Create a messages array for chat APIs"""
```

**Example Usage**:
```python
data = {"users": [...]}
prompt = create_llm_prompt(
    data,
    instruction="Analyze these users and suggest improvements:",
    format_as_toon=True
)
```

---

#### 3.2.7 `metrics.py`

**Purpose**: Compare token costs and provide conversion statistics

**Functions**:

```python
def count_tokens(text: str, model: str = "gpt-4") -> int:
    """
    Count tokens using tiktoken library.
    Support models: gpt-4, gpt-3.5-turbo, claude, etc.
    """

def compare_formats(data: Any) -> ComparisonResult:
    """
    Compare JSON vs TOON token counts and savings.
    Returns ComparisonResult with metrics.
    """

def generate_report(data: Any, output_format: str = "text") -> str:
    """
    Generate detailed comparison report.
    Formats: 'text', 'json', 'markdown'
    """
```

**Data Classes**:
```python
@dataclass
class ComparisonResult:
    json_tokens: int
    toon_tokens: int
    savings_tokens: int
    savings_percent: float
    json_size_bytes: int
    toon_size_bytes: int
    compression_ratio: float
```

**Dependencies**: Use `tiktoken` library for accurate token counting

---

#### 3.2.8 `cli.py`

**Purpose**: Provide command-line interface tools

**Commands**:

1. **`json2toon`**: Convert JSON to TOON
   ```bash
   json2toon input.json -o output.toon
   json2toon input.json --wrap-prompt --instruction "Analyze this data"
   ```

2. **`toon2json`**: Convert TOON to JSON
   ```bash
   toon2json input.toon -o output.json
   ```

3. **`json2toon-report`**: Generate comparison report
   ```bash
   json2toon-report input.json --model gpt-4 --format markdown
   ```

**Implementation Framework**: Use `typer` for type-safe CLI with auto-documentation

**Common Options**:
- `--config`: Path to config file
- `--verbose`: Enable verbose output
- `--quiet`: Suppress all output except errors
- `--output / -o`: Output file path (default: stdout)

---

#### 3.2.9 `core.py`

**Purpose**: Provide high-level convenience functions

**Functions**:

```python
def json_to_toon(data: Any, config: ToonConfig = None) -> str:
    """Convenience function for encoding"""

def toon_to_json(toon_str: str, config: ToonConfig = None) -> Any:
    """Convenience function for decoding"""

def convert_file(input_path: str, output_path: str, direction: str = "to_toon"):
    """Convert file from JSON to TOON or vice versa"""

def get_conversion_stats(data: Any) -> ComparisonResult:
    """Quick stats without full encoding"""
```

---

## 4. Implementation Guidelines

### 4.1 Python Standards

- **Version**: Python 3.8+ (use modern type hints)
- **Style**: Follow PEP 8, use `black` formatter
- **Type Hints**: Use throughout, validate with `mypy`
- **Docstrings**: Google style docstrings for all public functions
- **Imports**: Organize with `isort`

### 4.2 Type Hints Strategy

```python
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass

# Use specific types when possible
def encode_table(data: List[Dict[str, Any]]) -> str: ...

# Use Union for multiple acceptable types
def encode(data: Union[dict, list, str, int, float, bool, None]) -> str: ...

# Use Optional for nullable parameters
def analyze(data: Any, config: Optional[ToonConfig] = None) -> StructureInfo: ...
```

### 4.3 Error Handling Pattern

```python
try:
    result = encode_data(data)
except (KeyError, ValueError) as e:
    raise EncodingError(f"Failed to encode data: {e}") from e
except Exception as e:
    raise Json2ToonError(f"Unexpected error: {e}") from e
```

### 4.4 Testing Approach

#### Test Categories:

1. **Unit Tests**: Test individual functions in isolation
2. **Integration Tests**: Test module interactions
3. **Round-trip Tests**: JSON → TOON → JSON should match original
4. **Edge Case Tests**: Empty data, null values, deep nesting
5. **Performance Tests**: Large datasets, token counting accuracy

#### Key Test Scenarios:

```python
# Test uniform array detection
def test_uniform_array_detection():
    uniform = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
    non_uniform = [{"a": 1}, {"b": 2, "c": 3}]
    
# Test table encoding
def test_table_encoding():
    data = {"users": [{"id": 1, "name": "Alice"}]}
    toon = encode(data)
    assert "| id | name |" in toon
    
# Test round-trip conversion
def test_roundtrip():
    original = {"key": "value", "num": 42}
    toon = json_to_toon(original)
    restored = toon_to_json(toon)
    assert original == restored

# Test token counting
def test_token_savings():
    data = [{"id": i, "name": f"User{i}"} for i in range(100)]
    result = compare_formats(data)
    assert result.savings_percent > 0
```

### 4.5 Configuration Management

- Use `pyproject.toml` for project metadata and dependencies
- Support `.json2toon.yaml` config files in project directories
- Environment variable overrides: `JSON2TOON_MAX_DEPTH`, etc.

### 4.6 Dependencies

**Required**:
- `tiktoken`: Token counting for OpenAI models
- `typer`: CLI framework
- `rich`: Beautiful terminal output (optional, for CLI)

**Development**:
- `pytest`: Testing framework
- `black`: Code formatter
- `mypy`: Type checking
- `isort`: Import sorting
- `pytest-cov`: Coverage reports

---

## 5. Development Priorities

### Phase 1: MVP (Minimum Viable Product)
1. ✅ Project structure setup
2. ✅ `exceptions.py` - Define error types
3. ✅ `config.py` - Basic configuration
4. ✅ `analyzer.py` - Structure analysis (uniform array detection)
5. ✅ `encoder.py` - JSON → TOON (focus on tables)
6. ✅ `metrics.py` - Token counting
7. ✅ Basic tests for encoder and analyzer

### Phase 2: Decoding & CLI
1. ✅ `decoder.py` - TOON → JSON (subset support)
2. ✅ Round-trip tests
3. ✅ `cli.py` - Implement `json2toon` command
4. ✅ `cli.py` - Implement `json2toon-report` command

### Phase 3: Prompt Helpers & Polish
1. ✅ `prompt.py` - LLM prompt generation
2. ✅ `cli.py` - Implement `toon2json` command
3. ✅ `core.py` - Convenience functions
4. ✅ Complete test suite
5. ✅ Documentation and examples

### Phase 4: Optimization & Extension
1. ⚙️ Performance optimization for large datasets
2. ⚙️ Extended TOON syntax support in decoder
3. ⚙️ Additional model support in token counting
4. ⚙️ Configuration presets for common use cases

---

## 6. API Design Patterns

### 6.1 Encoder API

```python
from json2toon import ToonEncoder, ToonConfig

# Basic usage
encoder = ToonEncoder()
toon_str = encoder.encode({"key": "value"})

# With custom config
config = ToonConfig(indent_size=4, table_separator="|")
encoder = ToonEncoder(config)
toon_str = encoder.encode(data)

# Convenience function
from json2toon import json_to_toon
toon_str = json_to_toon(data)
```

### 6.2 Decoder API

```python
from json2toon import ToonDecoder

# Basic usage
decoder = ToonDecoder()
data = decoder.decode(toon_string)

# Convenience function
from json2toon import toon_to_json
data = toon_to_json(toon_string)
```

### 6.3 Metrics API

```python
from json2toon import compare_formats, generate_report

# Get comparison metrics
result = compare_formats(data)
print(f"Savings: {result.savings_percent}%")

# Generate detailed report
report = generate_report(data, output_format="markdown")
print(report)
```

### 6.4 Prompt Helper API

```python
from json2toon import create_llm_prompt

# Create prompt with TOON data
prompt = create_llm_prompt(
    data=my_data,
    instruction="Analyze the following user data:",
    format_as_toon=True,
    add_code_fence=True
)

# Send to LLM
response = openai.ChatCompletion.create(
    messages=[{"role": "user", "content": prompt}]
)
```

---

## 7. Token Counting Methodology

### 7.1 Approach

Use `tiktoken` library for accurate token counting:

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))
```

### 7.2 Model Support

- **OpenAI**: `gpt-4`, `gpt-3.5-turbo`, `text-davinci-003`
- **Anthropic**: Use `cl100k_base` encoding as approximation
- **Custom**: Allow custom encoding registration

### 7.3 Comparison Methodology

1. Serialize original data to JSON string (compact, no extra spaces)
2. Count JSON tokens using specified model encoding
3. Encode data to TOON format
4. Count TOON tokens using same encoding
5. Calculate savings: `(json_tokens - toon_tokens) / json_tokens * 100`

---

## 8. Integration Workflows

### 8.1 With LLM APIs

```python
import openai
from json2toon import create_llm_prompt

# Prepare data
user_data = load_user_data()

# Create TOON prompt
prompt = create_llm_prompt(
    data=user_data,
    instruction="Identify patterns in user behavior:"
)

# Send to OpenAI
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
```

### 8.2 With Data Pipelines

```python
from json2toon import ToonEncoder, compare_formats

# In ETL pipeline
def optimize_for_llm(data: dict) -> str:
    # Check if TOON saves tokens
    comparison = compare_formats(data)
    
    if comparison.savings_percent > 10:
        return json_to_toon(data)
    else:
        return json.dumps(data)
```

### 8.3 With Config Files

```python
# Save config for project
config = ToonConfig(
    indent_size=2,
    max_string_length=1000,
    uniformity_threshold=0.9
)
save_config(config, ".json2toon.yaml")

# Load in team's code
config = load_config(".json2toon.yaml")
encoder = ToonEncoder(config)
```

---

## 9. Code Quality Checklist

Before considering a module complete, ensure:

- ✅ All functions have type hints
- ✅ All public functions have docstrings (Google style)
- ✅ Error handling follows the exception hierarchy
- ✅ Unit tests cover main functionality
- ✅ Edge cases are handled (empty, null, deep nesting)
- ✅ Code passes `black`, `mypy`, `isort`
- ✅ No circular dependencies
- ✅ Performance is acceptable for datasets up to 10MB

---

## 10. Example TOON Outputs

### Example 1: User Directory

**Input JSON**:
```json
{
  "users": [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin"},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "user"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com", "role": "user"}
  ]
}
```

**Output TOON**:
```toon
users:
| id | name    | email               | role  |
|----|---------|---------------------|-------|
| 1  | Alice   | alice@example.com   | admin |
| 2  | Bob     | bob@example.com     | user  |
| 3  | Charlie | charlie@example.com | user  |
```

### Example 2: Nested Configuration

**Input JSON**:
```json
{
  "app": {
    "name": "MyApp",
    "version": "1.0.0",
    "database": {
      "host": "localhost",
      "port": 5432,
      "credentials": {
        "username": "admin",
        "password": "secret"
      }
    },
    "features": ["auth", "analytics", "api"]
  }
}
```

**Output TOON**:
```toon
app:
  name: MyApp
  version: 1.0.0
  database:
    host: localhost
    port: 5432
    credentials:
      username: admin
      password: secret
  features: [auth, analytics, api]
```

### Example 3: Mixed Data Types

**Input JSON**:
```json
{
  "summary": {
    "total": 150,
    "active": 120,
    "percentage": 80.0,
    "tags": ["important", "reviewed", "2024"],
    "details": [
      {"category": "A", "count": 50},
      {"category": "B", "count": 70},
      {"category": "C", "count": 30}
    ]
  }
}
```

**Output TOON**:
```toon
summary:
  total: 150
  active: 120
  percentage: 80.0
  tags: [important, reviewed, 2024]
  details:
  | category | count |
  |----------|-------|
  | A        | 50    |
  | B        | 70    |
  | C        | 30    |
```

---

## 11. Common Pitfalls & Solutions

### Pitfall 1: Over-optimization
**Problem**: Trying to optimize every structure  
**Solution**: Only use table format when uniformity > threshold AND row count > minimum

### Pitfall 2: Loss of Type Information
**Problem**: TOON doesn't explicitly mark types  
**Solution**: Decoder must infer types carefully (numbers, booleans, nulls, strings)

### Pitfall 3: Complex String Escaping
**Problem**: Strings with special characters break parsing  
**Solution**: Implement proper quoting rules or escaping in encoder/decoder

### Pitfall 4: Deep Nesting Performance
**Problem**: Recursive encoding of very deep structures  
**Solution**: Check `max_nesting_depth` config, raise error if exceeded

### Pitfall 5: Token Counting Inaccuracy
**Problem**: Different tokenizers give different counts  
**Solution**: Use `tiktoken` for OpenAI, document which encoding for other models

---

## 12. Future Extensions

### Possible Enhancements:
- 📊 **Visual diff tool**: Compare JSON vs TOON side-by-side
- 🔧 **Schema validation**: Validate TOON against JSON schema
- 🌐 **Multi-language support**: Ports to JavaScript, Rust, Go
- 📝 **IDE plugins**: Syntax highlighting for TOON format
- 🚀 **Streaming encoder**: Handle very large datasets
- 🔐 **Encryption support**: Secure sensitive fields in TOON

---

## 13. Quick Start for Implementation

### Step 1: Create Project Structure
```bash
mkdir -p src/json2toon tests
touch src/json2toon/{__init__.py,exceptions.py,config.py,analyzer.py,encoder.py,decoder.py,prompt.py,metrics.py,cli.py,core.py}
touch tests/{test_encoder.py,test_decoder.py,test_analyzer.py,test_metrics.py,test_prompt.py}
```

### Step 2: Start with Exceptions
Build the foundation with clear error types.

### Step 3: Build Config
Define configuration dataclass and load/save functions.

### Step 4: Implement Analyzer
This is critical - get uniform array detection right.

### Step 5: Build Encoder (MVP)
Focus on table format first, it provides the most value.

### Step 6: Add Metrics
Token counting validates the project's purpose.

### Step 7: Implement CLI
Make it usable from command line.

### Step 8: Add Decoder
Complete the round-trip capability.

### Step 9: Prompt Helpers
Polish the LLM integration story.

### Step 10: Test Everything
Comprehensive tests ensure reliability.

---

## 14. Success Criteria

The implementation is successful when:

✅ **Functional**: All core features work as documented  
✅ **Tested**: >90% code coverage with passing tests  
✅ **Token Efficient**: Demonstrates >20% savings on typical datasets  
✅ **Round-trip Accurate**: JSON → TOON → JSON preserves data  
✅ **Documented**: Clear API docs and examples  
✅ **Installable**: `pip install json2toon` works  
✅ **CLI Works**: All three commands function correctly  
✅ **Type Safe**: Passes mypy strict mode  
✅ **Clean Code**: Passes black, isort, and linting  
✅ **Performant**: Handles 10MB JSON files in <5 seconds  

---

**End of Agent Guide**

This document should provide everything needed to build json2toon from scratch with high quality and clear understanding of requirements.
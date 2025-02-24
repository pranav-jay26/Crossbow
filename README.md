# Crossbow 🏹

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
**High-performance data ingestion for scientific computing**

Crossbow is a Rust-powered data parsing library with Python bindings, designed for efficiently converting large Excel and CSV files into Apache Arrow format. Built with the Rust ecosystem's best practices and Python's scientific computing in mind.

## Features ✨

- 🚀 **Native-speed parsing** leveraging Rust's zero-copy operations
- 📊 **Multi-format support**: XLSX, XLS, ODS, and CSV
- 🏹 **Arrow-native output** for seamless Pandas/NumPy integration
- 🔍 **Automatic type inference** with fallback to string types
- 🧩 **Null-safe data handling** using Arrow's null bitmap system
- 📈 **Memory-efficient** streaming conversion
- 🐍 **Pythonic API** with full type hint support

## Usage

### Python API

```python
import crossbow as cxb
import pyarrow as pa

# Read Excel file (xlsx/xls/ods)
excel_batch = cxb.read_excel_py("data.xlsx", "Sheet1")
excel_table = pa.Table.from_batches([excel_batch])
excel_df = excel_table.to_pandas()

# Read CSV file
csv_batch = cxb.read_csv_py("data.csv")
csv_table = pa.Table.from_batches([csv_batch])
csv_df = csv_table.to_pandas()

print(f"Excel Data:\n{excel_df.head()}")
print(f"\nCSV Data:\n{csv_df.head()}")
```

### Command Line Interface

```bash
# Interactive mode (select file and sheet from current directory)
crossbow

# Process specific Excel file with sheet selection
crossbow --file data.xlsx --sheet Sheet1

# Process CSV file
crossbow --file data.csv

# Verbose mode for debugging
crossbow --file large_dataset.ods --verbose

# Output options (future implementation)
crossbow --file data.xlsx --output results.parquet
```

Key CLI Features:

- Interactive file/sheet selection
- Automatic format detection
- Progress indicators
- Error logging with stack traces
- Memory usage monitoring

## Architecture

```mermaid
graph LR
A[Excel/CSV File] --> B[Rust Parser]
B --> C[Arrow RecordBatch]
C --> D[Python Binding]
D --> E[Pandas DataFrame]
style B fill:#f0f0f0,stroke:#666
style C fill:#ffe4b2,stroke:#666
```

## Prerequisites

- Rust 1.70+ (via [rustup](https://rustup.rs/))
- Python 3.12

## Development Setup

### Clone the repository

```bash
git clone https://github.com/pranav-jay26/crossbow.git
```

### Create virtual environment

```bash
python3.12 -m venv .venv && source .venv/bin/activate
```

### Install build tools

```bash
pip install maturin pandas pyarrow
```

### Compile and install wheels

```bash
maturin develop --release
```

## Contributing

We welcome contributions! Please see our [Contribution Guidelines](CONTRIBUTING.md) for details.

Contributions are welcome! Please refer to these contribution guidelines:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open Pull Request

## License

Apache 2.0 - See [LICENSE](LICENSE) for details.

---

Developed with ❤️ by Pranav Jayakumar | Powered by [Apache Arrow](https://arrow.apache.org/) and [Rust](https://www.rust-lang.org/)

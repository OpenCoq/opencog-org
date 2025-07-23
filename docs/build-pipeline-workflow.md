# OpenCog Build Pipeline Issue Generator

This GitHub Actions workflow automatically creates GitHub issues for each component in the OpenCog ecosystem build pipeline.

## Usage

### Manual Trigger
1. Go to the "Actions" tab in the GitHub repository
2. Select "Create OpenCog Build Pipeline Issues" workflow
3. Click "Run workflow"
4. Optionally enable "Dry run mode" to preview what would be created without actually creating issues

### Automatic Execution
The workflow runs automatically on the 1st of each month at 8 AM UTC.

## What It Does

The workflow creates individual GitHub issues for each component in the OpenCog build pipeline, organized by layers:

### Foundation Layer
- **cogutil** - Core utilities

### Core Layer  
- **atomspace** - Main AtomSpace implementation
- **atomspace-rocks** - RocksDB storage backend
- **atomspace-restful** - RESTful API interface

### Logic Layer
- **unify** - Unification algorithms
- **ure** - Unified Rule Engine

### Cognitive Systems Layer
- **cogserver** - Server framework
- **attention** - Attention allocation system
- **spacetime** - Spatial and temporal reasoning

### Advanced Systems Layer
- **pln** - Probabilistic Logic Networks
- **miner** - Pattern mining system

### Learning Systems Layer
- **moses** - Meta-Optimizing Semantic Evolutionary Search
- **asmoses** - AtomSpace-based MOSES

### Language Processing Layer
- **lg-atomese** - Link Grammar integration
- **learn** - Language learning system
- **language-learning** - Language learning components

### Integration Layer
- **opencog** - Main integration package

## Issue Content

Each generated issue includes:
- Build steps with specific commands
- Dependency information
- Components that require this component
- Appropriate labels for filtering
- Automatic duplicate prevention

## Labels

Issues are tagged with:
- `build-pipeline` - All pipeline issues
- `{layer-name}` - Specific layer (e.g., `foundation-layer`, `core-layer`)
- `{component-name}` - Specific component (e.g., `cogutil`, `atomspace`)

## Features

- **Duplicate Prevention**: Checks for existing issues before creating new ones
- **Dry Run Mode**: Preview mode to see what would be created
- **Sequential Execution**: Respects dependency order
- **Comprehensive Coverage**: All major OpenCog components included
#!/usr/bin/env python
import sys
print("Python version:", sys.version)
print("Python path:")
for p in sys.path:
    print(f"  {p}")

print("\nTrying to import transformers...")
try:
    import transformers
    print(f"✓ transformers version: {transformers.__version__}")
    print(f"✓ transformers location: {transformers.__file__}")
except Exception as e:
    print(f"✗ Failed to import transformers: {e}")
    sys.exit(1)

print("\nTrying to import HfArgumentParser...")
try:
    from transformers import HfArgumentParser
    print("✓ HfArgumentParser imported successfully")
except Exception as e:
    print(f"✗ Failed to import HfArgumentParser: {e}")
    print(f"Available attributes in transformers:")
    attrs = [attr for attr in dir(transformers) if 'Arg' in attr]
    print(f"  Argument-related: {attrs}")
    
print("\nChecking transformers.__all__...")
if hasattr(transformers, '__all__'):
    if 'HfArgumentParser' in transformers.__all__:
        print("✓ HfArgumentParser is in transformers.__all__")
    else:
        print("✗ HfArgumentParser NOT in transformers.__all__")
        print(f"First 10 items in __all__: {transformers.__all__[:10]}")
else:
    print("transformers has no __all__ attribute")
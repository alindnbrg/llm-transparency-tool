import streamlit as st
import sys

st.title("Import Debug")

st.write("Python version:", sys.version)
st.write("Python executable:", sys.executable)

try:
    import transformers
    st.success(f"✓ transformers version: {transformers.__version__}")
    st.success(f"✓ transformers location: {transformers.__file__}")
except Exception as e:
    st.error(f"✗ Failed to import transformers: {e}")
    st.stop()

try:
    from transformers import HfArgumentParser
    st.success("✓ HfArgumentParser imported successfully")
except Exception as e:
    st.error(f"✗ Failed to import HfArgumentParser: {e}")
    st.write("Available attributes in transformers:")
    attrs = [attr for attr in dir(transformers) if 'Arg' in attr]
    st.write(f"  Argument-related: {attrs}")

st.write("Current working directory:", st.session_state.get('cwd', 'Not set'))

# Try to import the problematic line from app.py
try:
    st.write("Attempting the exact import from app.py...")
    exec("from transformers import HfArgumentParser")
    st.success("✓ Exact import from app.py works!")
except Exception as e:
    st.error(f"✗ Exact import from app.py failed: {e}")
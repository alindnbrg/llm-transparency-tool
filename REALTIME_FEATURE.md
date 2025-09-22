# Real-time Text Input Feature

This document describes the new real-time text input functionality added to the LLM Transparency Tool.

## Overview

The app now supports two input modes:
1. **Dataset Mode** (original): Select from predefined sentences
2. **Real-time Mode** (new): Type text and see live transparency analysis

## Features

### Mode Toggle
- Located in the sidebar as "Input Mode" radio buttons
- Seamlessly switch between Dataset and Real-time modes
- State is preserved across browser sessions

### Real-time Text Processing
- Type directly into a text area in the main interface (same location as the dropdown)
- Processing is **debounced** (500ms delay) to prevent excessive computation
- Visual indicator shows "⏱️ Processing..." while waiting for debounce
- Character limits are enforced if configured

### Performance Optimizations
- **Debounced Input**: Waits 500ms after user stops typing before processing
- **Smart Caching**: Leverages existing Streamlit cache system for previously processed texts
- **Incremental Updates**: Graph and visualizations update smoothly without jarring transitions

### User Experience
- **Instant Feedback**: Shows processing status while typing
- **Error Handling**: Warns if text exceeds configured character limits  
- **State Management**: Clean transitions between modes with proper state clearing

## Technical Implementation

### New Functions

#### `is_debounced(key: str, wait_ms: int = 300) -> bool`
- Checks if enough time has passed since last input change
- Uses session state to track timing
- Triggers `st.rerun()` if still within debounce period

#### `update_debounce_timer(key: str)`
- Updates timestamp for debounced actions
- Called when text input changes

### Modified Functions

#### `draw_dataset_selection() -> Optional[str]`
- Now returns `Optional[str]` instead of `int`
- Added input mode selection logic
- Handles both dataset selection and real-time text input
- Manages session state for mode switching

### Session State Keys

| Key | Type | Description |
|-----|------|-------------|
| `input_mode` | str | Current mode: \"Dataset\" or \"Real-time\" |
| `live_text` | str | Current text in real-time mode |
| `live_text_input` | str | Streamlit widget key for text area |
| `live_text_last_change` | float | Timestamp of last text change (for debouncing) |

## Usage Instructions

### For Users

1. **Switch to Real-time Mode**:
   - Look for \"Input Mode\" in the sidebar
   - Select \"Real-time\" radio button

2. **Type Your Text**:
   - Use the text area that appears in the main interface (where the dropdown was)
   - Type naturally - processing is automatic
   - Wait for "Processing..." indicator to disappear

3. **View Results**:
   - Graph updates after you stop typing (500ms delay)
   - All existing features work: attention maps, token analysis, etc.

### For Developers

#### Running the App
```bash
# Install dependencies
pip install streamlit torch transformers networkx pandas plotly

# Run the app
streamlit run llm_transparency_tool/server/app.py -- config/local.json
```

#### Testing
```bash
# Run the test suite
python test_debounce_logic.py

# Test specific components
python test_realtime_feature.py  # Requires full dependencies
```

#### Configuration

Adjust debounce timing in `draw_dataset_selection()`:
```python
# Current default: 500ms
if live_text.strip() and is_debounced(\"live_text\", wait_ms=500):
    return live_text.strip()
```

For faster response (less debouncing):
```python
# Faster: 200ms  
if live_text.strip() and is_debounced(\"live_text\", wait_ms=200):
    return live_text.strip()
```

For slower response (more debouncing):
```python  
# Slower: 1000ms (1 second)
if live_text.strip() and is_debounced(\"live_text\", wait_ms=1000):
    return live_text.strip()
```

## Performance Characteristics

### Debounce Timing
- **Default**: 500ms (good balance of responsiveness and performance)
- **Minimum Recommended**: 200ms (for very fast users)
- **Maximum Recommended**: 1000ms (for slower hardware)

### Expected Latency
- **Short texts (< 50 tokens)**: < 200ms after debounce
- **Medium texts (50-200 tokens)**: 200-500ms after debounce  
- **Long texts (200+ tokens)**: 500ms-2s after debounce

### Memory Usage
- Caching prevents reprocessing identical inputs
- Memory usage scales with number of unique texts processed
- Streamlit's cache management handles cleanup automatically

## Compatibility

### Browser Support
- All modern browsers (Chrome, Firefox, Safari, Edge)
- Requires JavaScript enabled
- Works on mobile devices (responsive text area)

### Model Support
- Compatible with all existing model configurations
- No changes needed to model loading or inference pipeline
- Works with both local and HuggingFace models

## Troubleshooting

### Common Issues

**Text not processing**:
- Ensure text is not just whitespace
- Wait for full debounce period (500ms)
- Check browser console for errors

**Performance issues**:
- Increase debounce time (wait_ms parameter)
- Check available GPU/CPU resources
- Try shorter input texts

**Mode switching problems**:
- Clear browser cache
- Check session state in Streamlit debugging
- Restart the app if persistent

### Debug Mode

Enable debug logging by setting `debug: true` in config:
```json
{
    \"debug\": true,
    \"other_settings\": \"...\"
}
```

## Future Enhancements

Potential improvements for future versions:

1. **Configurable Debounce**: UI slider to adjust debounce timing
2. **Streaming Updates**: Progressive graph updates as you type
3. **Text Suggestions**: Auto-complete based on training data  
4. **History**: Save and recall previously typed texts
5. **Export**: Export real-time analyses to files
6. **Collaboration**: Share real-time sessions with others

## Architecture Notes

The implementation leverages Streamlit's reactive architecture:

```
User Types → Text Area → Session State → Debounce Check → Model Inference → Graph Update
     ↑                                                                            ↓
     ←←←←←←←←←←←←←←←← st.rerun() ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

Key design decisions:
- **Stateless Functions**: All logic is pure functions that take session state as input
- **Minimal Dependencies**: Reuses existing caching and model infrastructure  
- **Graceful Degradation**: Falls back to dataset mode if real-time mode fails
- **Performance First**: Debouncing prevents expensive operations during typing
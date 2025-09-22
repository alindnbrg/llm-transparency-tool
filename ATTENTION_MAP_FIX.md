# Attention Map Container Fix

## Issue Fixed

The attention map and contribution map were not appearing in the frontend when users clicked on attention edges in the contribution graph.

## Root Cause

In the `draw_graph_and_selection` method of `/llm_transparency_tool/server/app.py`, the `draw_attn_info` method was being called with the wrong container parameter:

```python
# BEFORE (incorrect):
head = self.draw_attn_info(edge, container_graph)
```

However, the `draw_attn_info` method signature expects a `container_attention_map` parameter specifically for displaying the attention and contribution matrices:

```python
def draw_attn_info(self, edge: UiGraphEdge, container_attention_map) -> Optional[int]:
```

## Solution

1. **Created proper container**: Added `container_attention_map = container_graph.container()` to create a dedicated container for attention visualizations.

2. **Fixed method call**: Changed the call to pass the correct container:
   ```python
   # AFTER (correct):
   head = self.draw_attn_info(edge, container_attention_map)
   ```

## Technical Details

### Container Layout
The new layout structure in `draw_graph_and_selection`:

```
container_graph (left column of main layout)
├── container_graph_left (5/6 width) - Contains the contribution graph
├── container_graph_right (1/6 width) - Contains head/neuron selectors  
└── container_attention_map (full width) - Contains attention & contribution heatmaps
```

### Affected Methods
- `draw_graph_and_selection()` - Fixed container creation and method call
- `draw_attn_info()` - No changes needed, already expected correct parameter

### UI Impact
When users click on attention edges in the contribution graph, they will now see:
1. **Attention Map**: Shows attention weights between tokens for the selected head
2. **Contribution Map**: Shows contribution values between tokens for the selected head

Both maps appear below the main contribution graph in a side-by-side layout.

## Testing

The fix can be verified by:

1. Running the transparency tool: `streamlit run llm_transparency_tool/server/app.py -- config/local.json`
2. Loading a model and sentence
3. Clicking on attention edges in the contribution graph
4. Confirming that both attention and contribution heatmaps appear

## Files Modified

- `/llm_transparency_tool/server/app.py` - Lines 573 and 599
  - Added container creation: `container_attention_map = container_graph.container()`
  - Fixed method call: `head = self.draw_attn_info(edge, container_attention_map)`

## Commit Message

```
Fix attention map and contribution map display issue

- Fixed incorrect container parameter in draw_attn_info call
- Added proper container_attention_map creation
- Attention and contribution heatmaps now display when clicking attention edges

Resolves issue where attention maps were not available in frontend
```
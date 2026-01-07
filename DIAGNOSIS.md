# Modeling Mode Selection & Transform Controls Issue - DIAGNOSIS

## Problem Summary
You cannot select or transform individual **vertices, edges, and faces** with transform controls (move, scale, rotate) in modeling mode.

## Root Cause Analysis

### Issue 1: selectObject() Function Conflict
**Location:** `index.html` lines 17162-17273

The `selectObject()` function is designed for whole-object selection and **always attaches transformControls to the entire object**:

```javascript
if (selectedObject) {
    // ... 
    transformControls.attach(selectedObject); // ❌ PROBLEM: Attaches to WHOLE object
```

**Impact:** When you switch to modeling mode and select a vertex/edge/face, the `selectObject()` function is still being called somewhere, which overrides the modeling mode selection and attaches the gizmo to the entire mesh instead of the selected sub-element.

---

### Issue 2: Missing Integration Point
**Location:** `selectObject()` function (index.html)

The function has **NO AWARENESS** of modeling mode or whether a sub-element is selected:

- It doesn't check `if (isModelingMode)` before attaching to the whole object
- It doesn't check `if (selectedElements.length > 0)` to defer to modeling selection
- It always treats the selection as a whole object

---

### Issue 3: Dual Selection System Conflict
There are **TWO competing selection systems**:

1. **Object Selection System** (`selectObject()` in index.html)
   - Works with whole objects
   - Attaches transformControls to `selectedObject`
   
2. **Modeling Mode Selection System** (canvas-selection.js + nanite-ex.js)
   - Works with vertices, edges, faces  
   - Manages `selectedElements` array
   - Has `updateTransformControlsAttachment()` to attach to `transformPivot`

**The Problem:** Both systems are trying to control `transformControls`, causing conflicts.

---

### Issue 4: Canvas Selection System
**Location:** `canvas-selection.js` lines 1-150

The box selection system in canvas-selection.js:
- Only selects **whole objects** via `performBoxSelection()`
- Doesn't integrate with modeling mode vertex/edge/face selection
- Never calls into the modeling mode selection functions

---

## Current Flow (BROKEN)

1. User enters modeling mode ✅
2. User clicks on a vertex helper → `selectVertex()` called in nanite-ex.js ✅
3. Vertex is added to `selectedElements[]` ✅  
4. `updateTransformControlsAttachment()` called → Creates `transformPivot` ✅
5. **BUT THEN:** Somewhere, `selectObject()` gets called ❌
6. `selectObject()` attaches transformControls to the **whole `selectedObject`** ❌
7. The gizmo now controls the entire mesh, not the vertex ❌

---

## Why It Happens

Looking at `selectObject()`:

```javascript
function selectObject(newObject) {
    activeObject = newObject;
    selectedObject = newObject;  // ❌ This is set even in modeling mode
    
    if (selectedObject) {
        transformControls.attach(selectedObject); // ❌ Always attached to whole object
    }
}
```

This function doesn't differentiate between:
- **Normal mode selection** (select whole objects) 
- **Modeling mode selection** (select sub-elements)

---

## The Disconnect with Your selectObject Code

Your provided `selectObject()` function ends with:

```javascript
if (physicsSystem) {
    physicsSystem.setSelectedObject(selectedObject);
}
```

This function is **NOT modeling-mode aware**. It needs to:
1. Check if modeling mode is active
2. Check if modeling elements are selected
3. Defer to the modeling system's attachment logic

---

## Solution Strategy

The fix requires **4 key changes**:

### 1. Modify `selectObject()` to be modeling-aware
```javascript
function selectObject(newObject) {
    // ... existing code ...
    
    if (selectedObject) {
        // ❌ REMOVE or CONDITIONALLY apply:
        // transformControls.attach(selectedObject);
        
        // ✅ ADD modeling mode check:
        if (isModelingMode) {
            // Don't attach to whole object in modeling mode
            // The modeling system (updateTransformControlsAttachment) handles it
            return;
        } else {
            // Only attach in normal mode
            transformControls.attach(selectedObject);
        }
    }
}
```

### 2. Ensure modeling selection doesn't trigger `selectObject()`
- Check nanite-ex.js click handlers
- Make sure `selectVertex()`, `selectEdge()`, `selectFace()` DON'T call `selectObject()`

### 3. Integrate canvas-selection.js with modeling mode
- Modify `performBoxSelection()` to check for modeling mode
- If modeling mode, use modeling selection functions instead
- Only use object selection in normal mode

### 4. Create a unified attachment function
- Consolidate when/how transformControls attaches
- Have a single decision point that considers:
  - Is modeling mode active?
  - Are sub-elements selected? 
  - Otherwise, use whole object selection

---

## Files to Modify

1. **index.html** - `selectObject()` function (around line 17162)
   - Add modeling mode awareness
   
2. **nanite-ex.js** - `selectVertex()`, `selectEdge()`, `selectFace()` functions  
   - Ensure they don't trigger `selectObject()`
   - Verify they properly update transformControls via `updateTransformControlsAttachment()`
   
3. **canvas-selection.js** - `performBoxSelection()` function
   - Add modeling mode detection
   - Route to appropriate selection system

4. **Processing/smengine-modeling.js** - Mouse event handlers
   - Ensure click events properly route to modeling selection system

---

## Why Transform Controls Don't Work

Once transformControls is attached to the whole object (not the vertex pivot):
- Dragging the gizmo moves the entire mesh
- The vertex helper stays visible but doesn't move with the gizmo
- There's no actual vertex transformation happening
- Geometry doesn't update because the code expects `transformPivot`, not `selectedObject`

---

## Next Steps

1. ✅ Verify the exact flow when clicking a vertex in modeling mode
2. ✅ Find where `selectObject()` is being called in modeling context
3. ✅ Implement the fix to make `selectObject()` modeling-aware
4. ✅ Test that transformControls now attaches to `transformPivot` in modeling mode
5. ✅ Verify geometry updates work correctly

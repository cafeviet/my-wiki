<template>
  <div class="mermaid-viewer-wrapper" ref="wrapperRef">
    <!-- Inline Toolbar -->
    <div class="mermaid-viewer-toolbar">
      <div class="mermaid-toolbar-left">
        <span class="mermaid-badge">
          <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
            <line x1="3" y1="9" x2="21" y2="9"/>
            <line x1="9" y1="21" x2="9" y2="9"/>
          </svg>
          Sơ đồ Mermaid
        </span>
        <span class="mermaid-scale-indicator">{{ Math.round(scale * 100) }}%</span>
      </div>

      <div class="mermaid-toolbar-actions">
        <button 
          type="button" 
          class="mermaid-btn" 
          @click="zoomIn" 
          title="Phóng to (+)"
        >
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            <line x1="11" y1="8" x2="11" y2="14"/>
            <line x1="8" y1="11" x2="14" y2="11"/>
          </svg>
        </button>

        <button 
          type="button" 
          class="mermaid-btn" 
          @click="zoomOut" 
          title="Thu nhỏ (-)"
        >
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            <line x1="8" y1="11" x2="14" y2="11"/>
          </svg>
        </button>

        <button 
          type="button" 
          class="mermaid-btn" 
          @click="resetView" 
          title="Đặt lại kích thước"
        >
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
            <path d="M3 3v5h5"/>
          </svg>
        </button>

        <button 
          type="button" 
          class="mermaid-btn" 
          @click="copyCode" 
          :title="copied ? 'Đã sao chép mã!' : 'Sao chép mã Mermaid'"
        >
          <svg v-if="!copied" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#10b981" stroke-width="2">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
        </button>

        <button 
          type="button" 
          class="mermaid-btn" 
          @click="downloadSvg" 
          title="Tải ảnh vector SVG"
        >
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7 10 12 15 17 10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
        </button>

        <button 
          type="button" 
          class="mermaid-btn mermaid-btn-primary" 
          @click="openModal" 
          title="Phóng to toàn màn hình (Nhấp đúp chuột)"
        >
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="15 3 21 3 21 9"/>
            <polyline points="9 21 3 21 3 15"/>
            <line x1="21" y1="3" x2="14" y2="10"/>
            <line x1="3" y1="21" x2="10" y2="14"/>
          </svg>
          <span class="btn-text">Toàn màn hình</span>
        </button>
      </div>
    </div>

    <!-- Inline Diagram Viewport -->
    <div 
      class="mermaid-viewport" 
      ref="viewportRef"
      :class="{ 'is-dragging': isDragging, 'is-zoomed': scale > 1 }"
      :style="viewportStyleVars"
      @mousedown="startDrag"
      @dblclick="openModal"
    >
      <div 
        v-if="svg"
        class="mermaid-content"
        :style="contentTransformStyle"
        v-html="svg"
      ></div>
      <div v-else-if="error" class="mermaid-error">
        <p>⚠️ Không thể kết xuất sơ đồ Mermaid:</p>
        <pre>{{ error }}</pre>
      </div>
      <div v-else class="mermaid-loading">
        <span class="loading-spinner"></span>
        <span>Đang kết xuất sơ đồ...</span>
      </div>

      <div class="mermaid-zoom-hint" v-if="svg && scale === 1">
        🔍 Nhấp đúp để phóng to toàn màn hình • Có thể kéo hoặc bấm +/- để zoom
      </div>
    </div>

    <!-- Fullscreen Lightbox Modal -->
    <Teleport to="body" v-if="isMounted">
      <Transition name="mermaid-modal-fade">
        <div 
          v-if="isModalOpen" 
          :class="['mermaid-modal-backdrop', { 'is-dark-modal': isDarkModal }]"
          @keydown="handleModalKeydown"
          tabindex="0"
          ref="modalBackdropRef"
        >
          <!-- Modal Toolbar -->
          <div class="mermaid-modal-header" @mousedown.stop>
            <div class="modal-title">
              <span class="modal-badge">Toàn màn hình</span>
              <span class="modal-scale-info">{{ Math.round(modalScale * 100) }}%</span>
            </div>

            <div class="modal-controls">
              <button class="modal-btn" @click="modalZoomIn" title="Phóng to (+)">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"/>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                  <line x1="11" y1="8" x2="11" y2="14"/>
                  <line x1="8" y1="11" x2="14" y2="11"/>
                </svg>
              </button>
              <button class="modal-btn" @click="modalZoomOut" title="Thu nhỏ (-)">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"/>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                  <line x1="8" y1="11" x2="14" y2="11"/>
                </svg>
              </button>
              <button class="modal-btn" @click="modalReset100" title="Kích thước gốc 100%">100%</button>
              <button class="modal-btn" @click="modalResetFit" title="Vừa màn hình">Vừa khung</button>
              <button 
                class="modal-btn" 
                @click="isDarkModal = !isDarkModal" 
                :title="isDarkModal ? 'Chuyển sang nền trắng' : 'Chuyển sang nền tối'"
              >
                <span v-if="isDarkModal">☀️ Nền trắng</span>
                <span v-else>🌙 Nền tối</span>
              </button>
              <button class="modal-btn" @click="downloadSvg" title="Tải ảnh vector SVG">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="7 10 12 15 17 10"/>
                  <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
                <span class="btn-text">Tải SVG</span>
              </button>
              <button class="modal-btn modal-close-btn" @click="closeModal" title="Đóng (Esc)">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
                <span class="btn-text">Đóng</span>
              </button>
            </div>
          </div>

          <!-- Modal Body -->
          <div 
            class="mermaid-modal-body"
            ref="modalBodyRef"
            :class="{ 'is-dragging': isModalDragging }"
            :style="viewportStyleVars"
            @mousedown="startModalDrag"
            @wheel.prevent="handleModalWheel"
            @dblclick="toggleModalZoom"
          >
            <div 
              class="mermaid-modal-content"
              :style="modalContentTransformStyle"
              v-html="svg"
            ></div>
          </div>

          <!-- Footer Bar -->
          <div class="mermaid-modal-footer">
            <span>🖱️ Cuộn chuột để Phóng to/Thu nhỏ • Kéo chuột để Di chuyển • Nhấp đúp để đổi kích thước • Phím <b>Esc</b> để Đóng</span>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, toRaw } from "vue";
import { useData } from "vitepress";
import mermaid from "mermaid";

const props = defineProps({
  graph: {
    type: String,
    required: true,
  },
  id: {
    type: String,
    required: true,
  },
  class: {
    type: String,
    required: false,
    default: "mermaid",
  }
});

const isMounted = ref(false);
const svg = ref(null);
const error = ref(null);
const copied = ref(false);
const wrapperRef = ref(null);
const viewportRef = ref(null);

// Natural SVG dimensions
const naturalWidth = ref(null);
const naturalHeight = ref(null);

// Inline Pan & Zoom State
const scale = ref(1);
const pan = ref({ x: 0, y: 0 });
const isDragging = ref(false);
const dragStart = ref({ x: 0, y: 0 });

// Modal Lightbox State
const isModalOpen = ref(false);
const isDarkModal = ref(false);
const modalScale = ref(1.0);
const modalPan = ref({ x: 0, y: 0 });
const isModalDragging = ref(false);
const modalDragStart = ref({ x: 0, y: 0 });
const modalBackdropRef = ref(null);
const modalBodyRef = ref(null);

const { page } = useData();
const { frontmatter } = toRaw(page.value || {});
const mermaidPageTheme = frontmatter?.mermaidTheme || "";

let observer = null;

// CSS Variables for Natural Width/Height
const viewportStyleVars = computed(() => {
  return {
    "--mermaid-natural-width": naturalWidth.value ? `${naturalWidth.value}px` : "auto",
    "--mermaid-natural-height": naturalHeight.value ? `${naturalHeight.value}px` : "auto",
  };
});

// Transformations
const contentTransformStyle = computed(() => {
  return {
    transform: `translate(${pan.value.x}px, ${pan.value.y}px) scale(${scale.value})`,
    transformOrigin: "center center",
    transition: isDragging.value ? "none" : "transform 0.18s cubic-bezier(0.16, 1, 0.3, 1)"
  };
});

const modalContentTransformStyle = computed(() => {
  return {
    transform: `translate(${modalPan.value.x}px, ${modalPan.value.y}px) scale(${modalScale.value})`,
    transformOrigin: "center center",
    transition: isModalDragging.value ? "none" : "transform 0.12s ease-out"
  };
});

// Zoom Controls (Inline)
const zoomIn = () => {
  scale.value = Math.min(Number((scale.value + 0.25).toFixed(2)), 4.0);
};

const zoomOut = () => {
  scale.value = Math.max(Number((scale.value - 0.25).toFixed(2)), 0.5);
  if (scale.value <= 1) {
    pan.value = { x: 0, y: 0 };
  }
};

const resetView = () => {
  scale.value = 1;
  pan.value = { x: 0, y: 0 };
};

// Inline Dragging
const startDrag = (e) => {
  if (e.button !== 0) return;
  isDragging.value = true;
  dragStart.value = {
    x: e.clientX - pan.value.x,
    y: e.clientY - pan.value.y,
  };
  window.addEventListener("mousemove", onDrag);
  window.addEventListener("mouseup", stopDrag);
};

const onDrag = (e) => {
  if (!isDragging.value) return;
  pan.value = {
    x: e.clientX - dragStart.value.x,
    y: e.clientY - dragStart.value.y,
  };
};

const stopDrag = () => {
  isDragging.value = false;
  window.removeEventListener("mousemove", onDrag);
  window.removeEventListener("mouseup", stopDrag);
};

// Modal Dragging
const startModalDrag = (e) => {
  if (e.button !== 0) return;
  isModalDragging.value = true;
  modalDragStart.value = {
    x: e.clientX - modalPan.value.x,
    y: e.clientY - modalPan.value.y,
  };
  window.addEventListener("mousemove", onModalDrag);
  window.addEventListener("mouseup", stopModalDrag);
};

const onModalDrag = (e) => {
  if (!isModalDragging.value) return;
  modalPan.value = {
    x: e.clientX - modalDragStart.value.x,
    y: e.clientY - modalDragStart.value.y,
  };
};

const stopModalDrag = () => {
  isModalDragging.value = false;
  window.removeEventListener("mousemove", onModalDrag);
  window.removeEventListener("mouseup", stopModalDrag);
};

// Modal Wheel Zoom centered
const handleModalWheel = (e) => {
  const zoomFactor = e.deltaY < 0 ? 1.15 : 0.85;
  const newScale = Math.min(Math.max(modalScale.value * zoomFactor, 0.2), 6.0);
  modalScale.value = Number(newScale.toFixed(2));
};

// Modal Zoom Actions
const modalZoomIn = () => {
  modalScale.value = Math.min(Number((modalScale.value + 0.25).toFixed(2)), 6.0);
};

const modalZoomOut = () => {
  modalScale.value = Math.max(Number((modalScale.value - 0.25).toFixed(2)), 0.2);
};

const modalReset100 = () => {
  modalScale.value = 1.0;
  modalPan.value = { x: 0, y: 0 };
};

const modalResetFit = () => {
  if (naturalWidth.value && naturalHeight.value && typeof window !== "undefined") {
    const availWidth = window.innerWidth * 0.92;
    const availHeight = (window.innerHeight - 120) * 0.92;
    const fitScale = Math.min(availWidth / naturalWidth.value, availHeight / naturalHeight.value, 1.2);
    modalScale.value = Math.max(Number(fitScale.toFixed(2)), 0.2);
  } else {
    modalScale.value = 1.0;
  }
  modalPan.value = { x: 0, y: 0 };
};

const toggleModalZoom = () => {
  if (Math.abs(modalScale.value - 1.0) < 0.1) {
    modalResetFit();
  } else {
    modalReset100();
  }
};

// Open / Close Modal
const openModal = () => {
  isModalOpen.value = true;
  // Calculate pleasant initial modal scale
  modalResetFit();
  // If the diagram fits with scale < 0.85, set to 1.0 so user can read comfortably immediately
  if (modalScale.value < 0.85) {
    modalScale.value = 1.0;
  }
  document.body.style.overflow = "hidden";
  nextTick(() => {
    modalBackdropRef.value?.focus();
    window.addEventListener("keydown", handleModalKeydown);
  });
};

const closeModal = () => {
  isModalOpen.value = false;
  document.body.style.overflow = "";
  window.removeEventListener("keydown", handleModalKeydown);
};

const handleModalKeydown = (e) => {
  if (e.key === "Escape") closeModal();
  else if (e.key === "+" || e.key === "=") modalZoomIn();
  else if (e.key === "-") modalZoomOut();
  else if (e.key === "0") modalReset100();
};

// Copy Code
const copyCode = async () => {
  try {
    const raw = decodeURIComponent(props.graph);
    await navigator.clipboard.writeText(raw);
    copied.value = true;
    setTimeout(() => {
      copied.value = false;
    }, 2000);
  } catch (err) {
    console.error("Lỗi sao chép:", err);
  }
};

// Download SVG
const downloadSvg = () => {
  if (!svg.value) return;
  const cleanSvg = svg.value.replace(/<span style="display: none">[\w\W]*?<\/span>/, "");
  const blob = new Blob([cleanSvg], { type: "image/svg+xml;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `mermaid-${props.id || 'diagram'}.svg`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};

// Render Logic
const renderChart = async () => {
  if (typeof window === "undefined") return;
  
  try {
    const hasDarkClass = document.documentElement.classList.contains("dark");
    
    // Load virtual mermaid config if available
    let pluginConfig = {};
    try {
      const settings = await import("virtual:mermaid-config");
      if (settings?.default) pluginConfig = settings.default;
    } catch {
      // fallback
    }

    const mermaidConfig = {
      securityLevel: "loose",
      startOnLoad: false,
      theme: hasDarkClass ? "dark" : (mermaidPageTheme || "default"),
      flowchart: { useMaxWidth: false, htmlLabels: true },
      sequence: { useMaxWidth: false },
      gantt: { useMaxWidth: false },
      c4: { useMaxWidth: false },
      ...pluginConfig
    };
    if (hasDarkClass) mermaidConfig.theme = "dark";

    mermaid.initialize(mermaidConfig);
    
    const uniqueId = `mermaid-svg-${props.id || 'diag'}-${Math.random().toString(36).substring(2, 9)}`;
    const decodedGraph = decodeURIComponent(props.graph);
    
    const { svg: rawSvg } = await mermaid.render(uniqueId, decodedGraph);

    // Extract natural dimensions from viewBox or max-width
    const viewBoxMatch = rawSvg.match(/viewBox="[\d.-]+\s+[\d.-]+\s+([\d.-]+)\s+([\d.-]+)"/);
    if (viewBoxMatch) {
      naturalWidth.value = parseFloat(viewBoxMatch[1]);
      naturalHeight.value = parseFloat(viewBoxMatch[2]);
    } else {
      const maxWidthMatch = rawSvg.match(/max-width:\s*([\d.-]+)px/);
      if (maxWidthMatch) {
        naturalWidth.value = parseFloat(maxWidthMatch[1]);
      }
    }

    const salt = Math.random().toString(36).substring(7);
    svg.value = `${rawSvg} <span style="display: none">${salt}</span>`;
    error.value = null;
  } catch (err) {
    console.error("Mermaid render error:", err);
    error.value = err.message || String(err);
  }
};

onMounted(async () => {
  isMounted.value = true;
  await renderChart();

  // Watch for theme changes
  observer = new MutationObserver(async (mutations) => {
    for (const m of mutations) {
      if (m.attributeName === "class") {
        await renderChart();
        break;
      }
    }
  });
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });
});

onUnmounted(() => {
  if (observer) observer.disconnect();
  window.removeEventListener("keydown", handleModalKeydown);
  document.body.style.overflow = "";
});
</script>

<style scoped>
.mermaid-viewer-wrapper {
  position: relative;
  margin: 24px 0 32px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: #ffffff;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
  transition: border-color 0.25s, box-shadow 0.25s;
}

.dark .mermaid-viewer-wrapper {
  background: var(--vp-c-bg-soft);
}

.mermaid-viewer-wrapper:hover {
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 6px 24px rgba(99, 102, 241, 0.08);
}

/* Toolbar */
.mermaid-viewer-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.7);
  border-bottom: 1px solid var(--vp-c-divider);
  backdrop-filter: blur(8px);
}

.dark .mermaid-viewer-toolbar {
  background: rgba(24, 24, 27, 0.7);
}

.mermaid-toolbar-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.mermaid-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 2px 7px;
  border-radius: 6px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
}

.mermaid-scale-indicator {
  font-size: 11px;
  font-weight: 600;
  color: var(--vp-c-text-2);
  background: var(--vp-c-bg);
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid var(--vp-c-divider);
}

.mermaid-toolbar-actions {
  display: flex;
  align-items: center;
  gap: 4px;
}

.mermaid-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  height: 28px;
  padding: 0 8px;
  font-size: 12px;
  font-weight: 500;
  color: var(--vp-c-text-2);
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  user-select: none;
}

.mermaid-btn:hover {
  color: var(--vp-c-brand-1);
  border-color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
}

.mermaid-btn-primary {
  color: #fff !important;
  background: var(--vp-c-brand-1) !important;
  border-color: var(--vp-c-brand-1) !important;
}

.mermaid-btn-primary:hover {
  background: var(--vp-c-brand-3) !important;
}

.btn-text {
  margin-left: 2px;
  font-size: 11px;
}

/* Viewport */
.mermaid-viewport {
  position: relative;
  width: 100%;
  min-height: 220px;
  padding: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: auto;
  cursor: default;
  background-color: #ffffff;
  background-image: radial-gradient(#e2e8f0 1.2px, transparent 1.2px);
  background-size: 20px 20px;
}

.dark .mermaid-viewport {
  background-color: var(--vp-c-bg);
  background-image: radial-gradient(var(--vp-c-divider) 1px, transparent 1px);
}

.mermaid-viewport.is-zoomed {
  cursor: grab;
}

.mermaid-viewport.is-dragging {
  cursor: grabbing !important;
  user-select: none;
}

.mermaid-content {
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 100%;
}

:deep(svg) {
  height: auto;
  max-width: 100% !important;
  display: block;
}

/* When zoomed inline, unlock width so diagram renders at native resolution */
.mermaid-viewport.is-zoomed :deep(svg) {
  width: var(--mermaid-natural-width, auto) !important;
  max-width: none !important;
}

.mermaid-zoom-hint {
  position: absolute;
  bottom: 8px;
  right: 12px;
  font-size: 11px;
  color: var(--vp-c-text-3);
  background: var(--vp-c-bg);
  padding: 2px 8px;
  border-radius: 4px;
  border: 1px solid var(--vp-c-divider);
  pointer-events: none;
  opacity: 0.85;
}

.mermaid-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  color: var(--vp-c-text-2);
  font-size: 13px;
  padding: 40px;
}

.loading-spinner {
  width: 24px;
  height: 24px;
  border: 2px solid var(--vp-c-divider);
  border-top-color: var(--vp-c-brand-1);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.mermaid-error {
  padding: 20px;
  color: #ef4444;
  font-size: 13px;
  max-width: 100%;
}

.mermaid-error pre {
  margin-top: 8px;
  padding: 12px;
  background: rgba(239, 68, 68, 0.1);
  border-radius: 6px;
  overflow-x: auto;
}

/* Fullscreen Modal - Nền trắng sáng mặc định */
.mermaid-modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 999999;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  outline: none;
  user-select: none;
  color: #1e293b;
}

.mermaid-modal-header {
  height: 56px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e2e8f0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.modal-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 6px;
  background: var(--vp-c-brand-1, #6366f1);
  color: #ffffff;
  letter-spacing: 0.5px;
}

.modal-scale-info {
  font-size: 13px;
  font-weight: 600;
  color: #475569;
}

.modal-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.modal-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  height: 32px;
  padding: 0 10px;
  font-size: 12px;
  font-weight: 500;
  color: #334155;
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.modal-btn:hover {
  background: #f1f5f9;
  border-color: #94a3b8;
  color: #0f172a;
}

.modal-close-btn {
  background: #fee2e2 !important;
  border-color: #fca5a5 !important;
  color: #dc2626 !important;
  padding: 0 12px;
}

.modal-close-btn:hover {
  background: #fecaca !important;
  color: #b91c1c !important;
}

/* Modal Body */
.mermaid-modal-body {
  flex: 1;
  width: 100%;
  height: calc(100% - 96px);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  cursor: grab;
  background-color: #ffffff;
  background-image: radial-gradient(#cbd5e1 1.5px, transparent 1.5px);
  background-size: 24px 24px;
}

.mermaid-modal-body.is-dragging {
  cursor: grabbing !important;
}

.mermaid-modal-content {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.mermaid-modal-content :deep(svg) {
  width: var(--mermaid-natural-width, auto) !important;
  max-width: none !important;
  height: auto !important;
  background-color: #ffffff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.mermaid-modal-footer {
  height: 40px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #64748b;
  border-top: 1px solid #e2e8f0;
  background: #ffffff;
}

.mermaid-modal-footer b {
  color: #0f172a;
}

/* Chế độ Dark mode khi người dùng bấm nút đổi sang nền tối */
.mermaid-modal-backdrop.is-dark-modal {
  background: #0f172a;
  color: #f8fafc;
}

.mermaid-modal-backdrop.is-dark-modal .mermaid-modal-header {
  background: rgba(15, 23, 42, 0.95);
  border-bottom-color: rgba(255, 255, 255, 0.1);
}

.mermaid-modal-backdrop.is-dark-modal .modal-scale-info {
  color: #cbd5e1;
}

.mermaid-modal-backdrop.is-dark-modal .modal-btn {
  color: #e2e8f0;
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.15);
}

.mermaid-modal-backdrop.is-dark-modal .modal-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}

.mermaid-modal-backdrop.is-dark-modal .mermaid-modal-body {
  background-color: #0f172a;
  background-image: radial-gradient(rgba(255, 255, 255, 0.1) 1.5px, transparent 1.5px);
}

.mermaid-modal-backdrop.is-dark-modal .mermaid-modal-content :deep(svg) {
  background-color: transparent;
  box-shadow: none;
  border: none;
  filter: drop-shadow(0 12px 36px rgba(0, 0, 0, 0.45));
}

.mermaid-modal-backdrop.is-dark-modal .mermaid-modal-footer {
  background: #0f172a;
  border-top-color: rgba(255, 255, 255, 0.08);
  color: #94a3b8;
}

.mermaid-modal-backdrop.is-dark-modal .mermaid-modal-footer b {
  color: #f1f5f9;
}

/* Transitions */
.mermaid-modal-fade-enter-active,
.mermaid-modal-fade-leave-active {
  transition: opacity 0.25s ease;
}

.mermaid-modal-fade-enter-from,
.mermaid-modal-fade-leave-to {
  opacity: 0;
}
</style>

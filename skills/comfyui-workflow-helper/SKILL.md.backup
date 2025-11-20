# ComfyUI Workflow Helper Skill

Expert guidance for ComfyUI workflow creation, node configuration, and optimization.

## Capabilities

This skill provides expert assistance with:

1. **Workflow Setup & Management**
   - Creating custom workflows from scratch
   - Importing and modifying existing workflows
   - Workflow organization and structure
   - Node connection best practices

2. **Node Configuration**
   - Model loaders (Checkpoints, LoRAs, VAEs)
   - Samplers and schedulers
   - Conditioning nodes (prompts)
   - Image processing nodes
   - ControlNet integration

3. **Model Management**
   - Installing models (checkpoints, VAEs, text encoders, diffusion models)
   - Model organization in directories
   - Model format compatibility
   - OmniGen2 setup

4. **Performance Optimization**
   - VRAM management strategies
   - Batch processing optimization
   - Workflow efficiency improvements
   - Node caching strategies

5. **Troubleshooting**
   - Model loading errors
   - Node connection issues
   - OOM (Out of Memory) errors
   - Workflow execution failures

## Key Knowledge Base

### ComfyUI Directory Structure

```
/srv/comfyui/
├── models/
│   ├── checkpoints/          # SD models (.safetensors, .ckpt)
│   ├── vae/                  # VAE models
│   ├── loras/                # LoRA models
│   ├── text_encoders/        # Text encoder models
│   ├── diffusion_models/     # Diffusion models
│   ├── controlnet/           # ControlNet models
│   ├── upscale_models/       # Upscaler models
│   └── embeddings/           # Textual inversion embeddings
├── input/                    # Input images
├── output/                   # Generated images
└── custom_nodes/             # Custom node extensions
```

### Essential Nodes

**Loading Nodes:**
- `Load Checkpoint` - Load SD models
- `Load VAE` - Load VAE models
- `Load LoRA` - Load LoRA models

**Conditioning Nodes:**
- `CLIP Text Encode (Prompt)` - Positive and negative prompts
- `Conditioning Combine` - Merge multiple conditioning

**Sampling Nodes:**
- `KSampler` - Main sampler node
- `KSampler Advanced` - Advanced sampling control

**Image Nodes:**
- `VAE Decode` - Convert latent to image
- `VAE Encode` - Convert image to latent
- `Save Image` - Save output

**Model Nodes:**
- `Model Sampling Discrete` - Sampling configuration
- `Model Sampling SD3` - SD3-specific sampling

### OmniGen2 Setup

**Required Models:**
1. **VAE:** `ae.safetensors` → `/srv/comfyui/models/vae/`
2. **Text Encoder:** `qwen_2.5_vl_fp16.safetensors` → `/srv/comfyui/models/text_encoders/`
3. **Diffusion Model:** `omnigen2_fp16.safetensors` → `/srv/comfyui/models/diffusion_models/`

**Download Script:**
```bash
# Use the provided download script
/root/homelab/scripts/download-comfyui-omnigen2-models.sh

# Or manual download:
mkdir -p /srv/comfyui/models/{vae,text_encoders,diffusion_models}
wget -O /srv/comfyui/models/vae/ae.safetensors \
  "https://huggingface.co/Comfy-Org/Lumina_Image_2.0_Repackaged/resolve/main/split_files/vae/ae.safetensors"
# ... (similar for other models)
```

## Common Workflows

### Basic txt2img Workflow

**Nodes Required:**
1. Load Checkpoint
2. CLIP Text Encode (Prompt) x2 (positive & negative)
3. Empty Latent Image
4. KSampler
5. VAE Decode
6. Save Image

**Connection Flow:**
```
Load Checkpoint → CLIP (positive/negative) → KSampler
Empty Latent → KSampler → VAE Decode → Save Image
Load Checkpoint → VAE Decode
```

### img2img Workflow

**Additional Nodes:**
1. Load Image
2. VAE Encode

**Connection Flow:**
```
Load Image → VAE Encode → KSampler
(Rest similar to txt2img)
```

### ControlNet Workflow

**Additional Nodes:**
1. Load ControlNet Model
2. Apply ControlNet
3. Preprocessor nodes (depends on ControlNet type)

## Usage Examples

### Example 1: Setting Up OmniGen2

**User:** "Help me set up OmniGen2 in ComfyUI"

**Assistant Response:**
I'll guide you through setting up OmniGen2 in ComfyUI.

**Step 1: Download Models**

Run the download script:
```bash
bash /root/homelab/scripts/download-comfyui-omnigen2-models.sh
```

Or download manually:
- VAE: ae.safetensors → /srv/comfyui/models/vae/
- Text Encoder: qwen_2.5_vl_fp16.safetensors → /srv/comfyui/models/text_encoders/
- Diffusion Model: omnigen2_fp16.safetensors → /srv/comfyui/models/diffusion_models/

**Step 2: Restart ComfyUI**

```bash
# If using Docker:
docker restart comfyui-container

# If using systemd:
sudo systemctl restart comfyui

# If running manually:
# Stop and restart the ComfyUI process
```

**Step 3: Verify in WebUI**

1. Open ComfyUI web interface
2. Check that models appear in dropdowns:
   - VAE loader should show "ae.safetensors"
   - Text encoder nodes should show "qwen_2.5_vl_fp16.safetensors"
   - Diffusion model loader should show "omnigen2_fp16.safetensors"

**Step 4: Create Workflow**

Use OmniGen2-specific nodes:
- Load the OmniGen2 diffusion model
- Load Qwen text encoder
- Load Lumina VAE
- Configure sampler for OmniGen2

### Example 2: Creating a Basic Workflow

**User:** "How do I create a simple txt2img workflow in ComfyUI?"

**Assistant Response:**
I'll help you create a basic txt2img workflow.

**Nodes to Add:**

1. **Right-click → Add Node → loaders → Load Checkpoint**
   - Select your SD model

2. **Right-click → Add Node → conditioning → CLIP Text Encode (Prompt)** × 2
   - One for positive prompt
   - One for negative prompt

3. **Right-click → Add Node → latent → Empty Latent Image**
   - Set width: 512
   - Set height: 512
   - Batch size: 1

4. **Right-click → Add Node → sampling → KSampler**
   - Seed: -1 (random)
   - Steps: 20-40
   - CFG: 4.5 (for photorealism)
   - Sampler: dpmpp_2m_karras
   - Scheduler: karras

5. **Right-click → Add Node → latent → VAE Decode**

6. **Right-click → Add Node → image → Save Image**

**Connections:**

```
Load Checkpoint [MODEL] → KSampler [model]
Load Checkpoint [CLIP] → CLIP Text Encode (pos) [clip]
Load Checkpoint [CLIP] → CLIP Text Encode (neg) [clip]
Load Checkpoint [VAE] → VAE Decode [vae]

CLIP Text Encode (pos) [CONDITIONING] → KSampler [positive]
CLIP Text Encode (neg) [CONDITIONING] → KSampler [negative]

Empty Latent Image [LATENT] → KSampler [latent_image]

KSampler [LATENT] → VAE Decode [samples]
VAE Decode [IMAGE] → Save Image [images]
```

**Usage:**
1. Enter your prompt in positive CLIP Text Encode
2. Enter negative prompt in negative CLIP Text Encode
3. Click "Queue Prompt" to generate

### Example 3: Troubleshooting OOM Errors

**User:** "ComfyUI keeps crashing with out of memory errors. How do I fix this?"

**Assistant Response:**
OOM errors in ComfyUI can be resolved with these strategies:

**1. Reduce Resolution**
- Change Empty Latent Image dimensions:
  - From 768×768 → 512×512
  - From 1024×1024 → 768×768
- Lower resolution = less VRAM usage

**2. Reduce Batch Size**
- In Empty Latent Image node:
  - Set batch_size to 1
- Generate images one at a time

**3. Use VRAM-Efficient Models**
- Use pruned models (smaller file size)
- Use fp16 models instead of fp32
- Example: `v1-5-pruned-emaonly.safetensors` vs full versions

**4. ComfyUI Launch Args**
Add these flags when starting ComfyUI:
```bash
--lowvram          # Aggressive VRAM optimization
--medvram          # Moderate VRAM optimization
--normalvram       # Normal VRAM usage
--cpu              # Use CPU instead of GPU (slow but no VRAM)
```

**5. Clear Cache**
- Restart ComfyUI between generations
- Clear browser cache
- Delete temporary files

**6. Check Node Efficiency**
- Remove unnecessary nodes
- Avoid multiple simultaneous samplers
- Use single VAE decode instead of multiple

**For 2GB VRAM:**
- Stick to 512×512 resolution
- Use --lowvram flag
- Generate single images (batch=1)
- Use pruned/optimized models

## Best Practices

1. **Workflow Organization**
   - Group related nodes together
   - Use reroute nodes for clean connections
   - Add note nodes to document workflow sections
   - Save workflows with descriptive names

2. **Node Connections**
   - Always connect correct output to correct input types
   - Use color coding: MODEL, CLIP, VAE, CONDITIONING, LATENT, IMAGE
   - Double-check all connections before queuing

3. **Model Management**
   - Keep models organized in proper subdirectories
   - Use descriptive filenames
   - Delete unused models to save space
   - Verify checksums after downloading

4. **Performance**
   - Start with lower resolutions for testing
   - Use batch generation only when VRAM allows
   - Cache models by reusing same checkpoint across generations
   - Close other GPU applications

5. **Troubleshooting**
   - Check ComfyUI console for error messages
   - Verify model files are in correct directories
   - Ensure model formats are compatible
   - Test with simple workflow first

## Quick Reference

### KSampler Settings for Photorealism

```
seed: -1 (random)
steps: 20-40
cfg: 4.5 (photorealism breakthrough)
sampler_name: dpmpp_2m_karras
scheduler: karras
denoise: 1.0
```

### Resolution Limits by VRAM

| VRAM | Max Resolution | Batch Size |
|------|---------------|------------|
| 2GB | 512×512 | 1 |
| 4GB | 768×768 | 1-2 |
| 6GB | 1024×1024 | 1-2 |
| 8GB+ | 1024×1024+ | 2-4 |

### Common Node Shortcuts

- **Ctrl + Enter**: Queue Prompt
- **Ctrl + Shift + Enter**: Queue Prompt (front of queue)
- **Double Click**: Add node (search)
- **Ctrl + D**: Duplicate selected nodes
- **Delete**: Remove selected nodes

## Advanced Techniques

### Batch Processing

Use batch nodes to generate multiple variations:
```
Batch Size: 4 in Empty Latent Image
→ Generates 4 images per queue
```

### Seed Control

For consistent results:
```
Fixed Seed: Use specific number (e.g., 12345)
Random Seed: Use -1
Seed Increment: Batch Size controls seed increment
```

### LoRA Stacking

Apply multiple LoRAs:
```
Load Checkpoint → Load LoRA (1) → Load LoRA (2) → KSampler
Set strength: 0.5-1.0 per LoRA
```

## Additional Resources

- ComfyUI GitHub: https://github.com/comfyanonymous/ComfyUI
- Custom Nodes Registry: https://github.com/ltdrdata/ComfyUI-Manager
- OmniGen2 Documentation: Hugging Face model pages
- Download Script: `/root/homelab/scripts/download-comfyui-omnigen2-models.sh`

## When to Invoke This Skill

Invoke this skill when users ask about:
- ComfyUI workflow creation
- Node configuration and connections
- Model installation for ComfyUI
- OmniGen2 setup
- Workflow optimization
- VRAM management in ComfyUI
- Troubleshooting ComfyUI errors
- Sampler and scheduler settings
- ControlNet integration
- Batch processing in ComfyUI

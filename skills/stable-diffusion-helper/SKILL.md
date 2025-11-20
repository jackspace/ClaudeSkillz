# Stable Diffusion Helper Skill

Expert guidance for Stable Diffusion image generation, optimization, and troubleshooting.

## Capabilities

This skill provides expert assistance with:

1. **Model Installation & Management**
   - Installing SD models (base, Realistic Vision, ChilloutMix, etc.)
   - Model comparison and selection
   - VRAM optimization strategies
   - Docker container configuration

2. **Prompt Engineering**
   - Photorealistic prompt formulas
   - Reality-anchored prompting techniques
   - Negative prompt strategies (anti-cartoon shields)
   - Subject description best practices

3. **Settings Optimization**
   - CFG scale recommendations (breakthrough: 4.5 for photorealism)
   - Sampling steps optimization
   - Sampler selection for different use cases
   - Resolution strategies for limited VRAM

4. **ADetailer Configuration**
   - Face detection setup (face_yolov8n.pt)
   - Hand detection setup (hand_yolov8n.pt)
   - Multi-pass configuration (face + hands)
   - Custom ADetailer prompts for photorealism

5. **Troubleshooting**
   - Glossy/anime eyes fixes
   - Cartoonish/plastic skin solutions
   - OOM (Out of Memory) error resolution
   - Poor hand generation workarounds

## Key Knowledge Base

### Photorealism Breakthrough Configuration

**Critical Settings:**
- **CFG Scale: 4.5** (MOST IMPORTANT - lower than typical 7.0)
- Sampling Steps: 40
- Sampler: DPM++ 2M Karras
- Resolution: 512×512 (portraits), 512×768 or 768×512 (full-body)

**Main Prompt Template:**
```
RAW candid photograph, unfiltered reality, authentic skin texture with visible pores and fine lines, subsurface scattering, real human imperfections, natural uneven skin tone, professional photo shoot, [SUBJECT], documentary photography style, Leica M10, Summilux 50mm f/1.4, natural diffused lighting, overcast golden hour, real skin blemishes, subtle wrinkles, natural oiliness, lifelike, hyperrealistic not CGI, shot on Kodak Portra 400, muted colors, organic imperfections, tangible reality
```

**Negative Prompt (Anti-Cartoon Shield):**
```
cartoon, anime, 3D render, CGI, illustration, painting, drawing, airbrushed, smooth skin, plastic skin, doll-like, mannequin, wax figure, synthetic, artificial, digital art, cell shading, flat colors, oversaturated, oversharpened, unrealistic, fake, computer generated, video game, Unreal Engine, Unity, rendered, illustrated, drawn, painted, sketched, perfect skin, flawless skin, porcelain skin, baby smooth, blur tool, beauty filter, Facetune, Instagram filter, TikTok filter, makeup filter, ugly, distorted, deformed, bad anatomy, poorly drawn, extra limbs, disfigured, low quality, blurry
```

### Model Comparison

**SD 1.5 Base (v1-5-pruned-emaonly.safetensors):**
- Best for: Head/shoulder portraits
- VRAM: 1.3-1.5GB active
- CFG: 4.5-5.0 optimal
- Limitations: Poor full-body anatomy

**Realistic Vision V5.1 (realisticVisionV51.safetensors):**
- Best for: Full-body shots
- VRAM: 1.5-1.8GB active
- CFG: 3.5-5.0 optimal
- Strengths: Improved anatomy, better hands/feet

### VRAM Optimization Flags

For 2GB VRAM setups:
```bash
--lowvram --medvram --no-half-vae --enable-insecure-extension-access
```

### Common Issues & Solutions

**Problem: Glossy/Anime Eyes**
- Lower CFG to 4.5
- Add to ADetailer prompt: `matte finish eyes, natural iris texture`
- Add to ADetailer negative: `glossy eyes, shiny eyes, anime eyes`

**Problem: Cartoonish Skin**
- Lower CFG to 4.5 (CRITICAL)
- Emphasize: `visible pores, subsurface scattering, natural imperfections`
- Negative: `smooth skin, plastic skin, perfect skin, airbrushed`

**Problem: OOM Errors**
- Reduce resolution to 512×512
- Reduce batch size to 1-2
- Verify flags: `--lowvram --medvram`
- Disable Hires.fix

**Problem: Poor Hand Generation**
- Enable 2nd ADetailer tab with `hand_yolov8n.pt`
- Use hand-specific prompts
- Consider cropping hands out of frame
- Use img2img to refine hands separately

## Usage Examples

### Example 1: Portrait Setup

**User:** "Help me set up photorealistic portrait generation"

**Assistant Response:**
I'll help you configure photorealistic portrait generation. Here's the optimal setup:

**1. Model Selection:**
- Use SD 1.5 Base or Realistic Vision V5.1
- Both work well for portraits

**2. Settings:**
```
CFG Scale: 4.5 (CRITICAL - this is the breakthrough setting)
Steps: 40
Sampler: DPM++ 2M Karras
Resolution: 512×512
Batch Size: 4
```

**3. Prompt Formula:**
```
RAW candid photograph, unfiltered reality, authentic skin texture with visible pores and fine lines, subsurface scattering, real human imperfections, natural uneven skin tone, professional photo shoot, [your subject here], documentary photography style, Leica M10, Summilux 50mm f/1.4, natural diffused lighting, overcast golden hour, real skin blemishes, subtle wrinkles, natural oiliness, lifelike, hyperrealistic not CGI, shot on Kodak Portra 400, muted colors, organic imperfections, tangible reality
```

**4. Enable ADetailer:**
- Model: face_yolov8n.pt
- Positive prompt: `authentic human skin, visible pores, skin texture, fine lines, natural imperfections, subsurface scattering, realistic eyes with matte finish, natural iris texture, subtle eye moisture, lifelike pupils, soft catchlight`
- Negative prompt: `smooth skin, airbrushed, plastic skin, glossy eyes, shiny eyes, anime eyes, beauty filter`

This configuration achieves ~75% photorealistic success rate!

### Example 2: Fixing Glossy Eyes

**User:** "My generated portraits have glossy, anime-like eyes. How do I fix this?"

**Assistant Response:**
Glossy eyes are a common issue. Here's the fix:

**Critical Step: Lower CFG Scale to 4.5**
This is THE most important change. CFG 7.0+ produces glossy eyes.

**ADetailer Configuration:**
1. Enable ADetailer with face_yolov8n.pt
2. Add to ADetailer positive prompt:
   ```
   realistic eyes with matte finish, natural iris texture, subtle eye moisture, lifelike pupils, soft catchlight, natural eye appearance
   ```
3. Add to ADetailer negative prompt:
   ```
   glossy eyes, shiny eyes, glass eyes, reflective eyes, glowing eyes, anime eyes, oversaturated eyes, multiple catchlights
   ```

**Additional Tips:**
- Set inpaint denoising to 0.4
- Ensure detection confidence is at 0.3
- Generate multiple batches - consistency improves with these settings

This combination eliminates the glossy eye problem in ~90% of generations.

### Example 3: Full-Body Generation

**User:** "I want to generate full-body photorealistic images. What settings should I use?"

**Assistant Response:**
Full-body generation requires different settings than portraits:

**1. Model: Use Realistic Vision V5.1 (REQUIRED)**
SD 1.5 base struggles with full-body anatomy. RV5.1 is specifically trained for this.

**2. Settings:**
```
CFG Scale: 4.0 (lower than portrait's 4.5)
Steps: 30
Sampler: DPM++ SDE Karras
Resolution: 512×768 (vertical) or 768×512 (horizontal)
Batch Size: 2 (lower to avoid OOM)
```

**3. Prompt Adjustments:**
Add to your prompt:
```
full body shot, standing pose (or action pose), realistic hands and feet, natural body proportions
```

**4. Multi-Pass ADetailer:**

**Tab 1 (Face):**
- Model: face_yolov8n.pt
- Use standard face prompts

**Tab 2 (Hands):**
- Model: hand_yolov8n.pt
- Positive: `realistic hands, natural finger placement, correct anatomy, five fingers per hand, organic hand structure`
- Negative: `extra fingers, missing fingers, deformed hands, mutated hands, fused fingers, too many fingers`

**Success Rate:** ~60% (testing in progress)

**Important:** Test with single image first to verify no OOM errors before batch generation.

## Best Practices

1. **Always start with CFG 4.5** - This is the photorealism breakthrough
2. **Use ADetailer** - Essential for face quality
3. **Test resolution limits** - Higher res may OOM on 2GB VRAM
4. **Generate batches** - 4× gives better odds of great results
5. **Save successful seeds** - Reuse for consistency
6. **Lower CFG for higher res** - 768× images need CFG 4.0

## Quick Reference

| Use Case | Model | CFG | Steps | Resolution | Batch |
|----------|-------|-----|-------|------------|-------|
| Portrait | SD 1.5 / RV5.1 | 4.5 | 40 | 512×512 | 4 |
| Full-Body Vertical | RV5.1 | 4.0 | 30 | 512×768 | 2 |
| Full-Body Horizontal | RV5.1 | 4.0 | 30 | 768×512 | 2 |
| Documentary | SD 1.5 / RV5.1 | 4.5 | 35 | 512×512 | 4 |
| Film Photography | SD 1.5 / RV5.1 | 4.5 | 40 | 512×512 | 4 |

## Additional Resources

For complete documentation, see:
- Stable Diffusion Photorealism Guide
- Preset Configuration Files (6 ready-to-use JSON presets)
- AI-ML Infrastructure Documentation

## When to Invoke This Skill

Invoke this skill when users ask about:
- Stable Diffusion configuration
- Photorealistic image generation
- Prompt engineering for realism
- Fixing cartoonish/AI-looking results
- ADetailer setup
- VRAM optimization
- Model comparison
- Troubleshooting generation issues
- CFG scale problems
- Eye or skin texture issues

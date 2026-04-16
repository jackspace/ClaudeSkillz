---
name: cloudflare-images
description: "Expert guidance for Cloudflare Images API (upload, store, serve) and Image Transformations (resize, optimize any image via URL or Workers). Covers direct creator uploads, named/flexible variants, signed URLs for private images, responsive image patterns, and batch uploads. Use when uploading images to Cloudflare, setting up image CDN delivery, resizing or optimizing images (WebP/AVIF), implementing direct creator uploads with CORS-safe multipart/form-data, creating image variants, generating HMAC-SHA256 signed URLs, transforming images via Workers cf.image, or troubleshooting errors (5408, 9401-9413). Keywords: cloudflare images, imagedelivery.net, /cdn-cgi/image/, direct creator upload, image variants, flexible variants, signed urls, webp avif conversion, responsive images, batch upload, CORS direct upload, multipart/form-data, image optimization cloudflare."
license: MIT
---

# Cloudflare Images

**Status**: Production Ready ✅
**Last Updated**: 2025-10-26
**Dependencies**: Cloudflare account with Images enabled
**Latest Versions**: Cloudflare Images API v2

---

## Overview

Cloudflare Images provides two powerful features:

1. **Images API**: Upload, store, and serve images with automatic optimization and variants
2. **Image Transformations**: Resize, optimize, and transform any publicly accessible image

**Key Benefits**:
- Global CDN delivery
- Automatic WebP/AVIF conversion
- Variants for different use cases (up to 100)
- Direct creator upload (user uploads without API keys)
- Signed URLs for private images
- Transform any image via URL or Workers

---

## Quick Start (5 Minutes)

### 1. Enable Cloudflare Images

Log into Cloudflare dashboard → **Images** → Enable for your account.

Get your Account ID and create an API token with **Cloudflare Images: Edit** permissions.

**Why this matters:**
- Account ID and API token are required for all API operations
- Images Free plan includes limited transformations

### 2. Upload Your First Image

```bash
curl --request POST \
  --url https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/images/v1 \
  --header 'Authorization: Bearer <API_TOKEN>' \
  --header 'Content-Type: multipart/form-data' \
  --form 'file=@./image.jpg'
```

Response includes:
- `id`: Image ID for serving
- `variants`: Array of delivery URLs

**CRITICAL:**
- Use `multipart/form-data` encoding (NOT `application/json`)
- Image ID is automatically generated (or use custom ID)

### 3. Serve the Image

```html
<img src="https://imagedelivery.net/<ACCOUNT_HASH>/<IMAGE_ID>/public" />
```

Default `public` variant serves the image. Replace with your own variant names.

### 4. Enable Image Transformations

Dashboard → **Images** → **Transformations** → Select your zone → **Enable for zone**

Now you can transform ANY image:

```html
<img src="/cdn-cgi/image/width=800,quality=85/uploads/photo.jpg" />
```

**Why this matters:**
- Works on images stored OUTSIDE Cloudflare Images
- Automatic caching on Cloudflare's global network
- No additional storage costs

### 5. Transform via Workers (Advanced)

```typescript
export default {
  async fetch(request: Request): Promise<Response> {
    const imageURL = "https://example.com/image.jpg";

    return fetch(imageURL, {
      cf: {
        image: {
          width: 800,
          quality: 85,
          format: "auto" // WebP/AVIF for supporting browsers
        }
      }
    });
  }
};
```

---

## The 3-Feature System

### Feature 1: Images API (Upload & Storage)

Store images on Cloudflare's network and serve them globally.

**Upload Methods**:
1. **File Upload** - Upload files directly from your server
2. **Upload via URL** - Ingest images from external URLs
3. **Direct Creator Upload** - Generate one-time upload URLs for user uploads

**Serving Options**:
- Default domain: `imagedelivery.net`
- Custom domains: `/cdn-cgi/imagedelivery/...`
- Signed URLs: Private images with expiry tokens

**See**: `templates/upload-api-basic.ts`, `templates/direct-creator-upload-backend.ts`

### Feature 2: Image Transformations

Optimize and resize ANY image (stored in Images or external).

**Two Methods**:
1. **URL Transformations** - Special URL format
2. **Workers Transformations** - Programmatic control via fetch

**Common Transformations**:
- Resize: `width=800,height=600,fit=cover`
- Optimize: `quality=85,format=auto`
- Effects: `blur=10,sharpen=3`
- Crop: `gravity=face,zoom=0.5`

**See**: `templates/transform-via-url.ts`, `templates/transform-via-workers.ts`

### Feature 3: Variants

Predefined image sizes for different use cases.

**Named Variants** (up to 100):
- Create once, use everywhere
- Example: `thumbnail`, `avatar`, `hero`
- Consistent transformations

**Flexible Variants** (dynamic):
- Enable per account
- Use transformation params in URL
- Example: `w=400,sharpen=3`
- **Cannot use with signed URLs**

**See**: `templates/variants-management.ts`, `references/variants-guide.md`

---

## Images API - Upload Methods

### Method 1: File Upload (Basic)

```bash
curl --request POST \
  https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1 \
  --header "Authorization: Bearer <API_TOKEN>" \
  --header "Content-Type: multipart/form-data" \
  --form 'file=@./image.jpg' \
  --form 'requireSignedURLs=false' \
  --form 'metadata={"key":"value"}'
```

**Key Options**:
- `file`: Image file (required)
- `id`: Custom ID (optional, default auto-generated)
- `requireSignedURLs`: `true` for private images (default: `false`)
- `metadata`: JSON object (max 1024 bytes, not visible to end users)

**Response**: Returns `result` with `id`, `filename`, `uploaded`, `requireSignedURLs`, and `variants` array of delivery URLs.

**See**: `templates/upload-api-basic.ts`

### Method 2: Upload via URL

Ingest images from external sources without downloading first.

```bash
curl --request POST \
  https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1 \
  --header "Authorization: Bearer <API_TOKEN>" \
  --form 'url=https://example.com/image.jpg' \
  --form 'metadata={"source":"external"}'
```

**When to use**:
- Migrating images from another service
- Ingesting user-provided URLs
- Backing up images from external sources

**CRITICAL:**
- URL must be publicly accessible or authenticated
- Supports HTTP basic auth: `https://user:password@example.com/image.jpg`
- Cannot use both `file` and `url` in same request

**See**: `templates/upload-via-url.ts`

### Method 3: Direct Creator Upload ⭐

Generate one-time upload URLs for users to upload directly to Cloudflare (no API key exposure).

**Backend Endpoint** (generate upload URL):
```typescript
const response = await fetch(
  `https://api.cloudflare.com/client/v4/accounts/${accountId}/images/v2/direct_upload`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      requireSignedURLs: true,
      metadata: { userId: '12345' },
      expiry: '2025-10-26T18:00:00Z' // Optional: default 30min, max 6hr
    })
  }
);

const { uploadURL, id } = await response.json();
// Return uploadURL to frontend
```

**Frontend Upload**:
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]); // MUST be named 'file'
await fetch(uploadURL, { method: 'POST', body: formData }); // NO Content-Type header
```

**Why this matters:**
- No API key exposure to browser
- Users upload directly to Cloudflare (faster, no intermediary server)
- One-time URL expires after use or timeout
- Webhooks available for upload success/failure notifications

**CRITICAL CORS FIX**:
- ✅ **DO**: Use `multipart/form-data` encoding (let browser set header)
- ✅ **DO**: Name field `file` (NOT `image` or other names)
- ✅ **DO**: Call `/direct_upload` API from backend only
- ❌ **DON'T**: Set `Content-Type: application/json` or `image/jpeg`
- ❌ **DON'T**: Call `/direct_upload` from browser (CORS will fail)

**See**: `templates/direct-creator-upload-backend.ts`, `templates/direct-creator-upload-frontend.html`, `references/direct-upload-complete-workflow.md`

---

## Image Transformations

### URL Transformations

Transform images using a special URL format.

**URL Pattern**:
```
https://<ZONE>/cdn-cgi/image/<OPTIONS>/<SOURCE-IMAGE>
```

**Example**:
```html
<img src="/cdn-cgi/image/width=800,quality=85,format=auto/uploads/photo.jpg" />
```

**Common Options**:
- **Sizing**: `width=800`, `height=600`, `fit=cover`
- **Quality**: `quality=85` (1-100)
- **Format**: `format=auto` (WebP/AVIF auto-detection), `format=webp`, `format=jpeg`
- **Cropping**: `gravity=auto` (smart crop), `gravity=face`, `trim=10`
- **Effects**: `blur=10`, `sharpen=3`, `brightness=1.2`, `contrast=1.1`
- **Rotation**: `rotate=90`, `flip=h` (horizontal), `flip=v` (vertical)

**Fit Options**:
- `scale-down`: Shrink to fit (never enlarge)
- `contain`: Resize to fit within dimensions (preserve aspect ratio)
- `cover`: Resize to fill dimensions (may crop)
- `crop`: Crop to exact dimensions
- `pad`: Resize and add padding (use with `background` option)

**Format Auto-Detection**:
```html
<img src="/cdn-cgi/image/format=auto/image.jpg" />
```

Cloudflare serves:
- AVIF to browsers that support it (Chrome, Edge)
- WebP to browsers without AVIF support (Safari, Firefox)
- Original format (JPEG) as fallback

**See**: `templates/transform-via-url.ts`, `references/transformation-options.md`

### Workers Transformations

Programmatic image transformations with custom URL schemes via `cf.image` in `fetch()`.

```typescript
// Custom URL scheme: /images/thumbnail/photo.jpg → fetch from origin with transforms
return fetch(`https://storage.example.com/${imagePath}`, {
  cf: {
    image: { width: 300, height: 300, fit: 'cover', quality: 85 }
  }
});
```

**Content negotiation**: Check `Accept` header for `image/avif` or `image/webp` and set `format` accordingly (or use `format: 'auto'`).

**Why Workers Transformations**: Custom URL schemes, preset names (`thumbnail`, `avatar`), content negotiation, access control, dynamic sizing based on device type.

**See**: `templates/transform-via-workers.ts`, `references/transformation-options.md`

---

## Variants Management

### Named Variants (Up to 100)

Create predefined transformations for different use cases.

**Create via API**:
```bash
curl "https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1/variants" \
  --header "Authorization: Bearer <API_TOKEN>" \
  --header "Content-Type: application/json" \
  --data '{
    "id": "avatar",
    "options": {
      "fit": "cover",
      "width": 200,
      "height": 200,
      "metadata": "none"
    },
    "neverRequireSignedURLs": false
  }'
```

**Use in URLs**:
```html
<img src="https://imagedelivery.net/<ACCOUNT_HASH>/<IMAGE_ID>/avatar" />
```

**When to use**:
- Consistent image sizes across your app
- Private images (works with signed URLs)
- Simple, predictable URLs

**See**: `templates/variants-management.ts`

### Flexible Variants

Dynamic transformations using params in URL.

**Enable** (per account, one-time):
```bash
curl --request PATCH \
  https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1/config \
  --header "Authorization: Bearer <API_TOKEN>" \
  --header "Content-Type: application/json" \
  --data '{"flexible_variants": true}'
```

**Use in URLs**:
```html
<img src="https://imagedelivery.net/<ACCOUNT_HASH>/<IMAGE_ID>/w=400,sharpen=3" />
```

**When to use**:
- Dynamic sizing needs
- Public images only (cannot use with signed URLs)
- Rapid prototyping

**CRITICAL:**
- ❌ **Cannot use with `requireSignedURLs=true`**
- ✅ **Use named variants for private images**

**See**: `references/variants-guide.md`

---

## Signed URLs (Private Images)

Generate time-limited URLs for private images using HMAC-SHA256 tokens.

**URL Format**:
```
https://imagedelivery.net/<ACCOUNT_HASH>/<IMAGE_ID>/<VARIANT>?exp=<EXPIRY>&sig=<SIGNATURE>
```

**Key steps**: Import signing key via `crypto.subtle.importKey`, sign `{imageId}{variant}{expiry}` with HMAC-SHA256, hex-encode the signature, append `?exp=` and `&sig=` to the delivery URL.

**When to use**: User profile photos, paid content, temporary downloads, secure image delivery.

**See**: `templates/signed-urls-generation.ts`, `references/signed-urls-guide.md` for full implementation.

---

## Responsive Images

Serve optimal image sizes for different screen sizes using `srcset` and `sizes` attributes.

- **Named Variants**: Use variant names like `mobile`, `tablet`, `desktop` in srcset URLs
- **Flexible Variants**: Use `w=480,f=auto`, `w=768,f=auto`, etc. in srcset URLs
- **Art Direction**: Use `<picture>` with `<source media="...">` for different crops per breakpoint

**See**: `templates/responsive-images-srcset.html`, `references/responsive-images-patterns.md`

---

## Critical Rules

### Always Do

✅ Use `multipart/form-data` for Direct Creator Upload
✅ Name the file field `file` (not `image` or other names)
✅ Call `/direct_upload` API from backend only (NOT browser)
✅ Use HTTPS URLs for transformations (HTTP not supported)
✅ URL-encode special characters in image paths
✅ Enable transformations on zone before using `/cdn-cgi/image/`
✅ Use named variants for private images (signed URLs)
✅ Check `Cf-Resized` header for transformation errors
✅ Set `format=auto` for automatic WebP/AVIF conversion
✅ Use `fit=scale-down` to prevent unwanted enlargement

### Never Do

❌ Use `application/json` Content-Type for file uploads
❌ Call `/direct_upload` from browser (CORS will fail)
❌ Use flexible variants with `requireSignedURLs=true`
❌ Resize SVG files (they're inherently scalable)
❌ Use HTTP URLs for transformations (HTTPS only)
❌ Put spaces or unescaped Unicode in URLs
❌ Transform the same image multiple times in Workers (causes 9403 loop)
❌ Exceed 100 megapixels image size
❌ Use `/cdn-cgi/image/` endpoint in Workers (use `cf.image` instead)
❌ Forget to enable transformations on zone before use

---

## Known Issues Prevention

This skill prevents **13+** documented issues including CORS errors, upload timeouts, request loops, and URL format problems. Key issues to watch for:

- **CORS errors on direct upload**: Use `multipart/form-data` (let browser set header), name field `file`, call `/direct_upload` from backend only
- **Error 5408 (timeout)**: Compress images client-side, enforce max 10MB file size
- **Error 9403 (request loop)**: Never fetch Worker's own URL; always use external origin URL
- **Error 9406/9419 (invalid URL)**: Use HTTPS only, encode special characters with `encodeURIComponent()`
- **Flexible variants + signed URLs**: Incompatible; use named variants for private images

**See**: `known-issues-reference.md` for all 13 issues with code examples and community references.

---

## Bundled Resources

**Templates** (`templates/`): Copy-paste code for uploads (`upload-api-basic.ts`, `upload-via-url.ts`, `direct-creator-upload-backend.ts`, `direct-creator-upload-frontend.html`), transformations (`transform-via-url.ts`, `transform-via-workers.ts`), variants (`variants-management.ts`), signed URLs (`signed-urls-generation.ts`), responsive images (`responsive-images-srcset.html`), batch uploads (`batch-upload.ts`), and config (`wrangler-images-binding.jsonc`).

**References** (`references/`): Deep-dive docs for API endpoints (`api-reference.md`), transform params (`transformation-options.md`), variants (`variants-guide.md`), signed URLs (`signed-urls-guide.md`), direct upload workflow (`direct-upload-complete-workflow.md`), responsive patterns (`responsive-images-patterns.md`), format optimization (`format-optimization.md`), and error troubleshooting (`top-errors.md`).

**Scripts** (`scripts/`): `check-versions.sh` to verify API endpoints are current.

---

## Advanced Topics

- **Custom Domains**: Serve from your own domain via `/cdn-cgi/imagedelivery/` with Transform Rules
- **Batch API**: High-volume uploads via `batch.imagedelivery.net` with batch tokens
- **Webhooks**: Upload success/failure notifications for Direct Creator Upload

**See**: `advanced-topics-reference.md` for full setup details, troubleshooting guides, and setup checklist.

---

## Official Documentation

- **Cloudflare Images**: https://developers.cloudflare.com/images/
- **Get Started**: https://developers.cloudflare.com/images/get-started/
- **Upload Images**: https://developers.cloudflare.com/images/upload-images/
- **Direct Creator Upload**: https://developers.cloudflare.com/images/upload-images/direct-creator-upload/
- **Transform Images**: https://developers.cloudflare.com/images/transform-images/
- **Transform via URL**: https://developers.cloudflare.com/images/transform-images/transform-via-url/
- **Transform via Workers**: https://developers.cloudflare.com/images/transform-images/transform-via-workers/
- **Create Variants**: https://developers.cloudflare.com/images/manage-images/create-variants/
- **Serve Private Images**: https://developers.cloudflare.com/images/manage-images/serve-images/serve-private-images/
- **Troubleshooting**: https://developers.cloudflare.com/images/reference/troubleshooting/
- **API Reference**: https://developers.cloudflare.com/api/resources/images/

---

## Package Versions (Verified 2025-10-26)

**API Version**: v2 (for direct uploads), v1 (for standard uploads)

**No npm packages required** - uses native Cloudflare APIs

**Optional**:
- `@cloudflare/workers-types@latest` - TypeScript types for Workers

---

**Questions?** Check `references/top-errors.md`, verify setup steps, or consult [official docs](https://developers.cloudflare.com/images/).

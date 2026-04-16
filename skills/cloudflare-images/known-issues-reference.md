# Cloudflare Images - Known Issues Prevention

This skill prevents **13+** documented issues.

## Issue #1: Direct Creator Upload CORS Error

**Error**: `Access to XMLHttpRequest blocked by CORS policy: Request header field content-type is not allowed`

**Source**: [Cloudflare Community #345739](https://community.cloudflare.com/t/direct-image-upload-cors-error/345739), [#368114](https://community.cloudflare.com/t/cloudflare-images-direct-upload-cors-problem/368114)

**Why It Happens**: Server CORS settings only allow `multipart/form-data` for Content-Type header

**Prevention**:
```javascript
// ✅ CORRECT
const formData = new FormData();
formData.append('file', fileInput.files[0]);
await fetch(uploadURL, {
  method: 'POST',
  body: formData // Browser sets multipart/form-data automatically
});

// ❌ WRONG
await fetch(uploadURL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' }, // CORS error
  body: JSON.stringify({ file: base64Image })
});
```

## Issue #2: Error 5408 - Upload Timeout

**Error**: `Error 5408` after ~15 seconds of upload

**Source**: [Cloudflare Community #571336](https://community.cloudflare.com/t/images-direct-creator-upload-error-5408/571336)

**Why It Happens**: Cloudflare has 30-second request timeout; slow uploads or large files exceed limit

**Prevention**:
- Compress images before upload (client-side with Canvas API)
- Use reasonable file size limits (e.g., max 10MB)
- Show upload progress to user
- Handle timeout errors gracefully

```javascript
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

if (file.size > MAX_FILE_SIZE) {
  alert('File too large. Please select an image under 10MB.');
  return;
}
```

## Issue #3: Error 400 - Invalid File Parameter

**Error**: `400 Bad Request` with unhelpful error message

**Source**: [Cloudflare Community #487629](https://community.cloudflare.com/t/direct-creator-upload-returning-400/487629)

**Why It Happens**: File field must be named `file` (not `image`, `photo`, etc.)

**Prevention**:
```javascript
// ✅ CORRECT
formData.append('file', imageFile);

// ❌ WRONG
formData.append('image', imageFile); // 400 error
formData.append('photo', imageFile); // 400 error
```

## Issue #4: CORS Preflight Failures

**Error**: Preflight OPTIONS request blocked

**Source**: [Cloudflare Community #306805](https://community.cloudflare.com/t/cors-error-when-using-direct-creator-upload/306805)

**Why It Happens**: Calling `/direct_upload` API directly from browser (should be backend-only)

**Prevention**:
```
ARCHITECTURE:
Browser → Backend API → POST /direct_upload → Returns uploadURL → Browser uploads to uploadURL
```

Never expose API token to browser. Generate upload URL on backend, return to frontend.

## Issue #5: Error 9401 - Invalid Arguments

**Error**: `Cf-Resized: err=9401` - Required cf.image options missing or invalid

**Source**: [Cloudflare Images Docs - Troubleshooting](https://developers.cloudflare.com/images/reference/troubleshooting/)

**Why It Happens**: Missing required transformation parameters or invalid values

**Prevention**:
```typescript
// ✅ CORRECT
fetch(imageURL, {
  cf: {
    image: {
      width: 800,
      quality: 85,
      format: 'auto'
    }
  }
});

// ❌ WRONG
fetch(imageURL, {
  cf: {
    image: {
      width: 'large', // Must be number
      quality: 150 // Max 100
    }
  }
});
```

## Issue #6: Error 9402 - Image Too Large

**Error**: `Cf-Resized: err=9402` - Image too large or connection interrupted

**Source**: [Cloudflare Images Docs - Troubleshooting](https://developers.cloudflare.com/images/reference/troubleshooting/)

**Why It Happens**: Image exceeds maximum area (100 megapixels) or download fails

**Prevention**:
- Validate image dimensions before transforming
- Use reasonable source images (max 10000x10000px)
- Handle network errors gracefully

## Issue #7: Error 9403 - Request Loop

**Error**: `Cf-Resized: err=9403` - Worker fetching its own URL or already-resized image

**Source**: [Cloudflare Images Docs - Troubleshooting](https://developers.cloudflare.com/images/reference/troubleshooting/)

**Why It Happens**: Transformation applied to already-transformed image, or Worker fetches itself

**Prevention**:
```typescript
// ✅ CORRECT
if (url.pathname.startsWith('/images/')) {
  const originalPath = url.pathname.replace('/images/', '');
  const originURL = `https://storage.example.com/${originalPath}`;
  return fetch(originURL, { cf: { image: { width: 800 } } });
}

// ❌ WRONG
if (url.pathname.startsWith('/images/')) {
  // Fetches worker's own URL, causes loop
  return fetch(request, { cf: { image: { width: 800 } } });
}
```

## Issue #8: Error 9406/9419 - Invalid URL Format

**Error**: `Cf-Resized: err=9406` or `err=9419` - Non-HTTPS URL or URL has spaces/unescaped Unicode

**Source**: [Cloudflare Images Docs - Troubleshooting](https://developers.cloudflare.com/images/reference/troubleshooting/)

**Why It Happens**: Image URL uses HTTP (not HTTPS) or contains invalid characters

**Prevention**:
```typescript
// ✅ CORRECT
const imageURL = "https://example.com/images/photo%20name.jpg";

// ❌ WRONG
const imageURL = "http://example.com/images/photo.jpg"; // HTTP not allowed
const imageURL = "https://example.com/images/photo name.jpg"; // Space not encoded
```

Always use `encodeURIComponent()` for URL paths:
```typescript
const filename = "photo name.jpg";
const imageURL = `https://example.com/images/${encodeURIComponent(filename)}`;
```

## Issue #9: Error 9412 - Non-Image Response

**Error**: `Cf-Resized: err=9412` - Origin returned HTML instead of image

**Source**: [Cloudflare Images Docs - Troubleshooting](https://developers.cloudflare.com/images/reference/troubleshooting/)

**Why It Happens**: Origin server returns 404 page or error page (HTML) instead of image

**Prevention**:
```typescript
// Verify URL before transforming
const originResponse = await fetch(imageURL, { method: 'HEAD' });
const contentType = originResponse.headers.get('content-type');

if (!contentType?.startsWith('image/')) {
  return new Response('Not an image', { status: 400 });
}

return fetch(imageURL, { cf: { image: { width: 800 } } });
```

## Issue #10: Error 9413 - Max Image Area Exceeded

**Error**: `Cf-Resized: err=9413` - Image exceeds 100 megapixels

**Source**: [Cloudflare Images Docs - Troubleshooting](https://developers.cloudflare.com/images/reference/troubleshooting/)

**Why It Happens**: Source image dimensions exceed 100 megapixels (e.g., 10000x10000px)

**Prevention**:
- Validate image dimensions before upload
- Pre-process oversized images
- Reject images above threshold

```typescript
const MAX_MEGAPIXELS = 100;

if (width * height > MAX_MEGAPIXELS * 1_000_000) {
  return new Response('Image too large', { status: 413 });
}
```

## Issue #11: Flexible Variants + Signed URLs Incompatibility

**Error**: Flexible variants don't work with private images

**Source**: [Cloudflare Images Docs - Enable flexible variants](https://developers.cloudflare.com/images/manage-images/enable-flexible-variants/)

**Why It Happens**: Flexible variants cannot be used with `requireSignedURLs=true`

**Prevention**:
```typescript
// ✅ CORRECT - Use named variants for private images
await uploadImage({
  file: imageFile,
  requireSignedURLs: true // Use named variants: /public, /avatar, etc.
});

// ❌ WRONG - Flexible variants don't support signed URLs
// Cannot use: /w=400,sharpen=3 with requireSignedURLs=true
```

## Issue #12: SVG Resizing Limitation

**Error**: SVG files don't resize via transformations

**Source**: [Cloudflare Images Docs - SVG files](https://developers.cloudflare.com/images/transform-images/#svg-files)

**Why It Happens**: SVG is inherently scalable (vector format), resizing not applicable

**Prevention**:
```typescript
// SVGs can be served but not resized
// Use any variant name as placeholder
// https://imagedelivery.net/<HASH>/<SVG_ID>/public

// SVG will be served at original size regardless of variant settings
```

## Issue #13: EXIF Metadata Stripped by Default

**Error**: GPS data, camera settings removed from uploaded JPEGs

**Source**: [Cloudflare Images Docs - Transform via URL](https://developers.cloudflare.com/images/transform-images/transform-via-url/#metadata)

**Why It Happens**: Default behavior strips all metadata except copyright

**Prevention**:
```typescript
// Preserve metadata
fetch(imageURL, {
  cf: {
    image: {
      width: 800,
      metadata: 'keep' // Options: 'none', 'copyright', 'keep'
    }
  }
});
```

**Options**:
- `none`: Strip all metadata
- `copyright`: Keep only copyright tag (default for JPEG)
- `keep`: Preserve most EXIF metadata including GPS

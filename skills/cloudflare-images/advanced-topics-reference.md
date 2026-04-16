# Cloudflare Images - Advanced Topics & Troubleshooting

## Custom Domains

Serve images from your own domain instead of `imagedelivery.net`.

**URL Format**:
```
https://example.com/cdn-cgi/imagedelivery/<ACCOUNT_HASH>/<IMAGE_ID>/<VARIANT>
```

**Requirements**:
- Domain must be on Cloudflare (same account as Images)
- Proxied through Cloudflare (orange cloud)

**Custom Paths** (Transform Rules):

Rewrite `/images/...` to `/cdn-cgi/imagedelivery/...`:

1. Dashboard → Rules → Transform Rules → Rewrite URL
2. Match: `starts_with(http.request.uri.path, "/images/")`
3. Rewrite: `/cdn-cgi/imagedelivery/<ACCOUNT_HASH>${substring(http.request.uri.path, 7)}`

Now `/images/{id}/{variant}` → `/cdn-cgi/imagedelivery/{hash}/{id}/{variant}`

**See**: [Serve images from custom domains](https://developers.cloudflare.com/images/manage-images/serve-images/serve-from-custom-domains/)

## Batch API

High-volume uploads with batch tokens.

**Host**: `batch.imagedelivery.net` (instead of `api.cloudflare.com`)

**Usage**:
```bash
# Create batch token in dashboard: Images → Batch API

curl "https://batch.imagedelivery.net/images/v1" \
  --header "Authorization: Bearer <BATCH_TOKEN>" \
  --form 'file=@./image.jpg'
```

**When to use**:
- Migrating thousands of images
- Bulk upload workflows
- Automated image ingestion

**See**: `templates/batch-upload.ts`

## Webhooks

Receive notifications for upload success/failure (Direct Creator Upload only).

**Setup**:
1. Dashboard → Notifications → Destinations → Webhooks → Create
2. Enter webhook URL and test
3. Notifications → All Notifications → Add → Images → Select webhook

**Payload** (example):
```json
{
  "imageId": "2cdc28f0-017a-49c4-9ed7-87056c83901",
  "status": "uploaded",
  "metadata": {"userId": "12345"}
}
```

**When to use**:
- Update database after upload
- Trigger image processing pipeline
- Notify user of upload status

**See**: [Configure webhooks](https://developers.cloudflare.com/images/manage-images/configure-webhooks/)

---

## Troubleshooting

### Problem: Images not transforming

**Symptoms**: `/cdn-cgi/image/...` returns original image or 404

**Solutions**:
1. Enable transformations on zone: Dashboard → Images → Transformations → Enable for zone
2. Verify zone is proxied through Cloudflare (orange cloud)
3. Check source image is publicly accessible
4. Wait 5-10 minutes for settings to propagate

### Problem: Direct upload returns CORS error

**Symptoms**: `Access-Control-Allow-Origin` error in browser console

**Solutions**:
1. Use `multipart/form-data` encoding (let browser set Content-Type)
2. Don't call `/direct_upload` from browser; call from backend
3. Name file field `file` (not `image`)
4. Remove manual Content-Type header

### Problem: Worker transformations return 9403 loop error

**Symptoms**: `Cf-Resized: err=9403` in response headers

**Solutions**:
1. Don't fetch Worker's own URL (use external origin)
2. Don't transform already-resized images
3. Check URL routing logic to avoid loops

### Problem: Signed URLs not working

**Symptoms**: 403 Forbidden when accessing signed URL

**Solutions**:
1. Verify image uploaded with `requireSignedURLs=true`
2. Check signature generation (HMAC-SHA256)
3. Ensure expiry timestamp is in future
4. Verify signing key matches dashboard (Images → Keys)
5. Cannot use flexible variants with signed URLs (use named variants)

### Problem: Images uploaded but not appearing

**Symptoms**: Upload returns 200 OK but image not in dashboard

**Solutions**:
1. Check for `draft: true` in response (Direct Creator Upload)
2. Wait for upload to complete (check via GET `/images/v1/{id}`)
3. Verify account ID matches
4. Check for upload errors in webhooks

---

## Complete Setup Checklist

- [ ] Cloudflare account with Images enabled
- [ ] Account ID and API token obtained (Images: Edit permission)
- [ ] (Optional) Image transformations enabled on zone
- [ ] (Optional) Variants created for common use cases
- [ ] (Optional) Flexible variants enabled if dynamic sizing needed
- [ ] (Optional) Signing key obtained for private images
- [ ] (Optional) Webhooks configured for upload notifications
- [ ] (Optional) Custom domain configured with Transform Rules
- [ ] Upload method implemented (file, URL, or direct creator)
- [ ] Serving URLs tested (imagedelivery.net or custom domain)
- [ ] Transformations tested (URL or Workers)
- [ ] Error handling implemented (CORS, timeouts, size limits)

# Cloudflare Email Routing — Advanced Guide

## Send Email: Complete Guide

### Configuration

#### Single Destination (Simple)

```jsonc
{
  "send_email": [
    {
      "name": "EMAIL",
      "destination_address": "notifications@yourdomain.com"
    }
  ]
}
```

**Behavior**: All emails sent via `env.EMAIL` go to this address.

#### Multiple Destinations (Flexible)

```jsonc
{
  "send_email": [
    {
      "name": "EMAIL",
      "allowed_destination_addresses": [
        "notifications@yourdomain.com",
        "alerts@yourdomain.com",
        "user@gmail.com"
      ]
    }
  ]
}
```

**Behavior**: Can send to any address in the list.

#### Multiple Bindings (Organized)

```jsonc
{
  "send_email": [
    {
      "name": "NOTIFICATIONS",
      "destination_address": "notifications@yourdomain.com"
    },
    {
      "name": "ALERTS",
      "destination_address": "alerts@yourdomain.com"
    }
  ]
}
```

**Behavior**: Use different bindings for different purposes.

---

### Sending Emails

#### Basic Text Email

```typescript
import { EmailMessage } from 'cloudflare:email';
import { createMimeMessage } from 'mimetext';

const msg = createMimeMessage();
msg.setSender({ name: 'My App', addr: 'noreply@yourdomain.com' });
msg.setRecipient('user@example.com');
msg.setSubject('Welcome!');
msg.addMessage({
  contentType: 'text/plain',
  data: 'Welcome to our service!',
});

const email = new EmailMessage(
  'noreply@yourdomain.com',
  'user@example.com',
  msg.asRaw()
);

await env.EMAIL.send(email);
```

#### HTML Email

```typescript
import { EmailMessage } from 'cloudflare:email';
import { createMimeMessage } from 'mimetext';

const msg = createMimeMessage();
msg.setSender({ name: 'My App', addr: 'noreply@yourdomain.com' });
msg.setRecipient('user@example.com');
msg.setSubject('Welcome!');

// Add both plain text and HTML versions
msg.addMessage({
  contentType: 'text/plain',
  data: 'Welcome to our service!',
});

msg.addMessage({
  contentType: 'text/html',
  data: '<h1>Welcome!</h1><p>Thanks for joining us.</p>',
});

const email = new EmailMessage(
  'noreply@yourdomain.com',
  'user@example.com',
  msg.asRaw()
);

await env.EMAIL.send(email);
```

#### Email with Custom Headers

```typescript
import { EmailMessage } from 'cloudflare:email';
import { createMimeMessage } from 'mimetext';

const msg = createMimeMessage();
msg.setSender({ name: 'My App', addr: 'noreply@yourdomain.com' });
msg.setRecipient('user@example.com');
msg.setSubject('Password Reset');

// Add custom headers
msg.setHeader('X-Priority', '1');
msg.setHeader('X-Application-ID', 'my-app-123');

msg.addMessage({
  contentType: 'text/plain',
  data: 'Click here to reset your password...',
});

const email = new EmailMessage(
  'noreply@yourdomain.com',
  'user@example.com',
  msg.asRaw()
);

await env.EMAIL.send(email);
```

---

## DNS Configuration

### Automatic Setup (Recommended)

When you enable Email Routing in the dashboard, Cloudflare automatically adds:

1. **MX Records** - Direct email to Cloudflare's servers
   ```
   yourdomain.com. 300 IN MX 13 amir.mx.cloudflare.net.
   yourdomain.com. 300 IN MX 86 linda.mx.cloudflare.net.
   yourdomain.com. 300 IN MX 24 isaac.mx.cloudflare.net.
   ```

2. **SPF Record** - Authorize Cloudflare to send on your behalf
   ```
   yourdomain.com. 300 IN TXT "v=spf1 include:_spf.mx.cloudflare.net ~all"
   ```

3. **DKIM Records** - Sign outgoing emails
   ```
   Automatically configured per domain
   ```

### Manual Setup (Advanced)

If you need to migrate from another provider:

1. Go to **Email > Email Routing > Settings**
2. Select **Start disabling > Unlock records and continue**
3. Edit DNS records as needed
4. When ready, **Lock DNS records** to protect Email Routing

**WARNING**: Changing MX records will break Email Routing. Only do this if migrating providers.

---

## Known Issues Prevention

This skill prevents **8 documented issues**:

### Issue #1: "Email Trigger not available to this workers"

**Error**: Testing email workers fails with "Email Trigger not available to this workers"

**Source**: [workers-sdk #3751](https://github.com/cloudflare/workers-sdk/issues/3751)

**Why It Happens**: Wrangler dev doesn't fully support email triggers; testing must be done via deployed Workers

**Prevention**:
- Always deploy email workers before testing
- Use `wrangler tail` for live debugging
- Use dashboard "Test Email Event" feature (when working)

---

### Issue #2: Destination Address Verification Bug

**Error**: Verified destination addresses show as "unverified" in Email Worker forwarding

**Source**: Community reports ([Cloudflare Community](https://community.cloudflare.com/t/email-worker-free-reliability/486680))

**Why It Happens**: Bug in dashboard where addresses only show verified if also used in regular routing rules

**Prevention**:
- Create a regular forward rule for each destination address first
- Then use the same addresses in Email Workers
- Verify addresses before deploying workers

---

### Issue #3: Gmail Rate Limiting

**Error**: "421: Our system has detected an unusual rate of unsolicited mail originating from your IP address"

**Source**: Community reports

**Why It Happens**: Gmail may flag Cloudflare's IP ranges as suspicious due to shared infrastructure

**Prevention**:
- Implement proper SPF/DKIM/DMARC records
- Don't send bulk emails through Email Routing
- Use transactional email services (e.g., SendGrid, Mailgun) for high volume
- Rate-limit your sending (max 50-100 emails/hour for personal use)

---

### Issue #4: SPF Permerror with MailChannels

**Error**: SPF permerror when routing through MailChannels

**Source**: [Community discussion](https://community.cloudflare.com/t/worker-mailchannels-email-routing-spf-permerror/637766)

**Why It Happens**: SPF record chain breaks when forwarding through multiple services

**Prevention**:
- Use Email Routing's native send capabilities instead of MailChannels
- If using MailChannels, configure SPF includes correctly
- Test with [MXToolbox SPF checker](https://mxtoolbox.com/spf.aspx)

---

### Issue #5: Limited Logging on Free Plan

**Error**: Cannot see worker logs or email processing details

**Source**: Community reports

**Why It Happens**: Free plan has limited log retention and streaming

**Prevention**:
- Use `wrangler tail` during development for live logs
- Use `console.log()` extensively in email workers
- Store critical data in D1/KV for debugging
- Upgrade to Workers Paid plan for better observability

---

### Issue #6: Activity Log Discrepancies

**Error**: Emails show as "Dropped" in Activity Log even when successfully forwarded

**Source**: Community reports

**Why It Happens**: Dashboard bug showing incorrect status

**Prevention**:
- Check actual email delivery instead of relying on dashboard
- Use `wrangler tail` to verify processing
- Implement your own logging in D1/KV
- Test with real emails to confirm delivery

---

### Issue #7: Test Email Event Loading Indefinitely

**Error**: Dashboard "Test Email Event" button remains in loading state forever

**Source**: [workers-sdk #9195](https://github.com/cloudflare/workers-sdk/issues/9195)

**Why It Happens**: Bug in dashboard testing interface (unresolved as of 2025-10)

**Prevention**:
- Don't rely on dashboard testing feature
- Use `curl` with local development instead
- Deploy and test with real emails
- Use `wrangler tail` to monitor processing

---

### Issue #8: Worker Call Failures

**Error**: "Rejected reason: Unknown error: failed to call worker: Worker call failed for 3 times, aborting…"

**Source**: [workers-sdk #9069](https://github.com/cloudflare/workers-sdk/issues/9069), Community reports

**Why It Happens**: Worker crashes due to runtime errors, timeouts, or memory issues

**Prevention**:
- Add comprehensive error handling with try/catch
- Set timeouts for external API calls
- Log errors to D1/KV before rejecting
- Use `ctx.waitUntil()` for non-critical operations
- Test with various email formats (plain text, HTML, attachments)

---

## Local Development

### Receiving Emails

Wrangler simulates email reception via HTTP POST:

```bash
# Start dev server
npx wrangler dev

# In another terminal, send test email
curl http://localhost:8787 -X POST \
  --data-binary @- << EOF
From: sender@example.com
To: recipient@yourdomain.com
Subject: Test Email

This is a test email body.
EOF
```

**What happens**: Wrangler logs the email processing and shows where forwarded emails would go.

### Sending Emails

Wrangler writes sent emails to local .eml files:

```typescript
// Your worker code
await env.EMAIL.send(message);
```

**Output in terminal**:
```
[wrangler:inf] send_email binding called with the following message:
  /tmp/miniflare-abc123/files/email/message-123.eml
```

**View the email**:
```bash
cat /tmp/miniflare-abc123/files/email/message-123.eml
```

---

## Configuration Files Reference

### Complete wrangler.jsonc (Both Receive + Send)

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "email-worker",
  "main": "src/email.ts",
  "account_id": "YOUR_ACCOUNT_ID",
  "compatibility_date": "2025-10-11",
  "observability": {
    "enabled": true
  },

  // Send email binding
  "send_email": [
    {
      "name": "NOTIFICATIONS",
      "destination_address": "notifications@yourdomain.com"
    },
    {
      "name": "ALERTS",
      "allowed_destination_addresses": [
        "alerts@yourdomain.com",
        "admin@yourdomain.com"
      ]
    }
  ],

  // Optional: Add other bindings
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "email-archive",
      "database_id": "YOUR_DATABASE_ID"
    }
  ],

  "kv_namespaces": [
    {
      "binding": "EMAIL_CACHE",
      "id": "YOUR_KV_ID"
    }
  ]
}
```

---

## TypeScript Types

### Environment Bindings

```typescript
interface Env {
  // Send email bindings
  EMAIL: SendEmail;
  NOTIFICATIONS: SendEmail;
  ALERTS: SendEmail;

  // Other bindings
  DB: D1Database;
  EMAIL_CACHE: KVNamespace;
}

interface SendEmail {
  send(message: EmailMessage): Promise<void>;
}
```

### Full Type Definitions

```typescript
import { EmailMessage } from 'cloudflare:email';

interface ForwardableEmailMessage {
  readonly from: string;
  readonly to: string;
  readonly headers: Headers;
  readonly raw: ReadableStream;
  readonly rawSize: number;

  setReject(reason: string): void;
  forward(rcptTo: string, headers?: Headers): Promise<void>;
  reply(message: EmailMessage): Promise<void>;
}

declare module 'cloudflare:email' {
  export class EmailMessage {
    constructor(from: string, to: string, raw: string | ReadableStream);
  }
}
```

---

## Advanced Topics

### Parsing Email Attachments

```typescript
import PostalMime from 'postal-mime';

export default {
  async email(message, env, ctx) {
    const parser = new PostalMime.default();
    const email = await parser.parse(await new Response(message.raw).arrayBuffer());

    // Access attachments
    if (email.attachments && email.attachments.length > 0) {
      for (const attachment of email.attachments) {
        console.log('Attachment:', attachment.filename);
        console.log('Type:', attachment.mimeType);
        console.log('Size:', attachment.content.length);

        // Store in R2
        await env.BUCKET.put(
          `emails/${Date.now()}-${attachment.filename}`,
          attachment.content
        );
      }
    }

    await message.forward('inbox@yourdomain.com');
  },
};
```

---

### Email-Based Task Creation

```typescript
import PostalMime from 'postal-mime';

export default {
  async email(message, env, ctx) {
    const parser = new PostalMime.default();
    const email = await parser.parse(await new Response(message.raw).arrayBuffer());

    // Extract task from email subject
    const taskMatch = email.subject.match(/\[TASK\](.*)/i);

    if (taskMatch) {
      const taskDescription = taskMatch[1].trim();

      // Create task in D1
      await env.DB.prepare(
        'INSERT INTO tasks (description, created_by, created_at) VALUES (?, ?, ?)'
      ).bind(
        taskDescription,
        message.from,
        new Date().toISOString()
      ).run();

      // Send confirmation
      await message.reply(new EmailMessage(
        'tasks@yourdomain.com',
        message.from,
        `Task created: ${taskDescription}`
      ));
    }
  },
};
```

---

### Email-Triggered Workflows

```typescript
export default {
  async email(message, env, ctx) {
    // Trigger Cloudflare Workflow based on email
    if (message.from.endsWith('@trusted-domain.com')) {
      await env.WORKFLOW.create({
        params: {
          emailFrom: message.from,
          emailTo: message.to,
          receivedAt: new Date().toISOString(),
        },
      });
    }

    await message.forward('inbox@yourdomain.com');
  },
};
```

---

## Complete Setup Checklist

### Email Routing Setup
- [ ] Domain is on Cloudflare DNS
- [ ] Email Routing enabled in dashboard
- [ ] MX, SPF, DKIM records automatically added
- [ ] At least one destination address verified
- [ ] Test basic forwarding with a custom address

### Email Workers (Receiving)
- [ ] `postal-mime@2.5.0` installed
- [ ] `mimetext@3.0.27` installed
- [ ] Email worker created with `async email()` handler
- [ ] Worker deployed: `npx wrangler deploy`
- [ ] Worker bound to email route in dashboard
- [ ] Test with real email to route address
- [ ] Verify logs with `wrangler tail`

### Send Email (Sending)
- [ ] `send_email` binding configured in `wrangler.jsonc`
- [ ] `destination_address` or `allowed_destination_addresses` specified
- [ ] All destination addresses verified in Email Routing
- [ ] Worker code uses `env.EMAIL.send()`
- [ ] Worker deployed: `npx wrangler deploy`
- [ ] Test sending email via Worker endpoint
- [ ] Confirm email delivery to recipient

---

## Troubleshooting

### Problem: "Email Trigger not available to this workers"

**Solution**:
- Deploy your worker: `npx wrangler deploy`
- Test with real emails, not local simulation
- Use `wrangler tail` to monitor processing

### Problem: "Destination address not verified"

**Solution**:
- Check Email Routing > Destination addresses in dashboard
- Click "Resend verification" if needed
- Create a regular forwarding rule first (workaround for bug)
- Verify all addresses before deploying workers

### Problem: Gmail rejects emails with 421 error

**Solution**:
- Verify SPF/DKIM records are configured (automatic with Email Routing)
- Reduce sending rate (max 50-100/hour for personal use)
- Don't send unsolicited emails or bulk mail
- Consider transactional email service for high volume

### Problem: Emails not forwarding from Email Worker

**Solution**:
- Check worker is bound to correct email route in dashboard
- Verify destination address is verified
- Use `wrangler tail` to see processing logs
- Check for errors in worker code (try/catch around forward())
- Confirm MX records are still pointing to Cloudflare

### Problem: Cannot see worker logs

**Solution**:
- Use `wrangler tail --format pretty` for live logs
- Add extensive `console.log()` statements in worker
- Store debug info in D1 or KV for later inspection
- Upgrade to Workers Paid plan for better log retention

### Problem: Worker crashes with "failed to call worker"

**Solution**:
- Add try/catch error handling around all operations
- Set timeouts for external API calls
- Test with different email formats (plain text, HTML, attachments)
- Check worker doesn't exceed CPU/memory limits
- Use `ctx.waitUntil()` for non-blocking operations

---

## Dependencies

**Required**:
- `postal-mime@2.5.0` - Parse incoming email messages
- `mimetext@3.0.27` - Create email messages for sending

**Built-in**:
- `cloudflare:email` - EmailMessage class (no installation needed)

**Optional**:
- `@cloudflare/workers-types` - TypeScript type definitions

---

## Official Documentation

- **Email Routing**: https://developers.cloudflare.com/email-routing/
- **Email Workers**: https://developers.cloudflare.com/email-routing/email-workers/
- **Send Email**: https://developers.cloudflare.com/email-routing/email-workers/send-email-workers/
- **Runtime API**: https://developers.cloudflare.com/email-routing/email-workers/runtime-api/
- **Local Development**: https://developers.cloudflare.com/email-routing/email-workers/local-development/
- **postal-mime**: https://www.npmjs.com/package/postal-mime
- **mimetext**: https://www.npmjs.com/package/mimetext

---

## Package Versions (Verified 2025-10-23)

```json
{
  "dependencies": {
    "postal-mime": "^2.5.0",
    "mimetext": "^3.0.27"
  },
  "devDependencies": {
    "@cloudflare/workers-types": "^4.20251014.0",
    "wrangler": "^4.44.0"
  }
}
```

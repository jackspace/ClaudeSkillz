---
name: cloudflare-email-routing
description: "Complete guide for Cloudflare Email Routing covering Email Workers (receiving emails) and Send Email bindings (sending emails from Workers). Use when setting up email routing, creating email workers, processing incoming emails, sending emails from Workers, implementing allowlists/blocklists, forwarding emails with custom logic, auto-replying, parsing email content, configuring MX/SPF/DKIM records, or troubleshooting email delivery issues. Prevents 8 documented issues including \"Email Trigger not available\" errors, destination address verification bugs, Gmail rate limiting, SPF permerror, worker call failures, and test event loading issues. Keywords: Cloudflare Email Routing, Email Workers, postal-mime, mimetext, cloudflare:email, EmailMessage, ForwardableEmailMessage, email forwarding, email allowlist, email blocklist, send_email binding, wrangler email, MX records, SPF, DKIM, email routing worker."
license: MIT
---

# Cloudflare Email Routing

**Status**: Production Ready
**Last Updated**: 2025-10-23
**Latest Versions**: postal-mime@2.5.0, mimetext@3.0.27

Cloudflare Email Routing provides two complementary capabilities:

1. **Email Workers** - Receive and process incoming emails with custom logic (allowlists, blocklists, forwarding, parsing, replying)
2. **Send Email** - Send emails from Workers to verified destination addresses (notifications, alerts, confirmations)

Both capabilities are **free** and work together to enable complete email functionality in Cloudflare Workers.

> For detailed configuration, known issues, advanced topics, and troubleshooting, see `references/advanced-guide.md`.

---

## Quick Start

### Step 1: Enable Email Routing (Dashboard)

**Prerequisites**: Domain must be on Cloudflare DNS

1. Cloudflare Dashboard > select domain > **Email** > **Email Routing**
2. Select **Enable Email Routing** > **Add records and enable** (auto-adds MX, SPF, DKIM)
3. Create a destination address (e.g., `hello@yourdomain.com` > `you@gmail.com`) and verify it

### Step 2: Create an Email Worker (Receiving)

Install dependencies:

```bash
npm install postal-mime@2.5.0 mimetext@3.0.27
```

Create `src/email.ts`:

```typescript
import { EmailMessage } from 'cloudflare:email';
import PostalMime from 'postal-mime';

export default {
  async email(message, env, ctx) {
    const parser = new PostalMime.default();
    const email = await parser.parse(await new Response(message.raw).arrayBuffer());

    console.log('From:', message.from);
    console.log('Subject:', email.subject);

    await message.forward('your-email@example.com');
  },
};
```

Configure `wrangler.jsonc`:

```jsonc
{
  "name": "email-worker",
  "main": "src/email.ts",
  "compatibility_date": "2025-10-11"
}
```

Deploy and bind: `npx wrangler deploy`, then Dashboard > Email > Email Routing > Email Workers > create route.

### Step 3: Send Emails from Workers

Add `send_email` binding to `wrangler.jsonc`:

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

**CRITICAL**: `destination_address` must be a verified address in Email Routing settings.

Send from your worker:

```typescript
import { EmailMessage } from 'cloudflare:email';
import { createMimeMessage } from 'mimetext';

export default {
  async fetch(request, env, ctx) {
    const msg = createMimeMessage();
    msg.setSender({ name: 'My App', addr: 'noreply@yourdomain.com' });
    msg.setRecipient('user@example.com');
    msg.setSubject('Welcome to My App');
    msg.addMessage({ contentType: 'text/plain', data: 'Thank you for signing up!' });

    const message = new EmailMessage('noreply@yourdomain.com', 'user@example.com', msg.asRaw());
    await env.EMAIL.send(message);

    return new Response('Email sent!');
  },
};
```

---

## Runtime API

```typescript
export default {
  async email(message: ForwardableEmailMessage, env: Env, ctx: ExecutionContext) {
    // message.from, message.to, message.headers, message.raw, message.rawSize
    // message.setReject(reason), message.forward(rcptTo), message.reply(emailMessage)
  },
};
```

---

## Common Patterns

### Allowlist

```typescript
export default {
  async email(message, env, ctx) {
    const allowList = ['friend@example.com', 'coworker@company.com'];
    if (!allowList.includes(message.from)) {
      message.setReject('Address not on allowlist');
      return;
    }
    await message.forward('inbox@yourdomain.com');
  },
};
```

### Blocklist

```typescript
export default {
  async email(message, env, ctx) {
    const blockList = ['spam@badactor.com', '@suspicious-domain.com'];
    if (blockList.some(pattern => message.from.includes(pattern))) {
      message.setReject('Sender blocked');
      return;
    }
    await message.forward('inbox@yourdomain.com');
  },
};
```

### Parse and Store (D1)

```typescript
import PostalMime from 'postal-mime';

export default {
  async email(message, env, ctx) {
    const parser = new PostalMime.default();
    const email = await parser.parse(await new Response(message.raw).arrayBuffer());

    await env.DB.prepare(
      'INSERT INTO emails (from_addr, subject, text, received_at) VALUES (?, ?, ?, ?)'
    ).bind(message.from, email.subject, email.text, new Date().toISOString()).run();

    await message.forward('inbox@yourdomain.com');
  },
};
```

### Auto-Reply

```typescript
import PostalMime from 'postal-mime';
import { createMimeMessage } from 'mimetext';
import { EmailMessage } from 'cloudflare:email';

export default {
  async email(message, env, ctx) {
    const parser = new PostalMime.default();
    const email = await parser.parse(await new Response(message.raw).arrayBuffer());

    const msg = createMimeMessage();
    msg.setSender({ name: 'Support', addr: 'support@yourdomain.com' });
    msg.setRecipient(message.from);
    msg.setHeader('In-Reply-To', message.headers.get('Message-ID'));
    msg.setSubject(`Re: ${email.subject}`);
    msg.addMessage({ contentType: 'text/plain', data: `Thanks for your message. We'll respond within 24 hours.` });

    await message.reply(new EmailMessage('support@yourdomain.com', message.from, msg.asRaw()));
    await message.forward('team@yourdomain.com');
  },
};
```

### Conditional Routing

```typescript
import PostalMime from 'postal-mime';

export default {
  async email(message, env, ctx) {
    const parser = new PostalMime.default();
    const email = await parser.parse(await new Response(message.raw).arrayBuffer());
    const subject = email.subject.toLowerCase();

    if (subject.includes('urgent') || subject.includes('critical')) {
      await message.forward('oncall@yourdomain.com');
    } else if (subject.includes('invoice') || subject.includes('payment')) {
      await message.forward('billing@yourdomain.com');
    } else {
      await message.forward('inbox@yourdomain.com');
    }
  },
};
```

---

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Email Trigger not available" | Deploy worker first (`npx wrangler deploy`), test with real emails |
| Destination address not verified | Create a regular forwarding rule first, then use in Workers |
| Gmail 421 rate limit error | Check SPF/DKIM, reduce rate to <100/hour, use transactional service for bulk |
| Emails not forwarding | Verify worker is bound to route, destination verified, MX records intact |
| No worker logs | Use `wrangler tail --format pretty`, add `console.log()`, store debug in D1/KV |
| "Failed to call worker" | Add try/catch, set timeouts, use `ctx.waitUntil()` for non-critical ops |

> For full known issues documentation and advanced troubleshooting, see `references/advanced-guide.md`.

---

## Dependencies

- `postal-mime@2.5.0` - Parse incoming emails
- `mimetext@3.0.27` - Create emails for sending
- `cloudflare:email` - EmailMessage class (built-in, no install needed)

## Official Documentation

- [Email Routing](https://developers.cloudflare.com/email-routing/)
- [Email Workers](https://developers.cloudflare.com/email-routing/email-workers/)
- [Send Email](https://developers.cloudflare.com/email-routing/email-workers/send-email-workers/)
- [Runtime API](https://developers.cloudflare.com/email-routing/email-workers/runtime-api/)
- [Local Development](https://developers.cloudflare.com/email-routing/email-workers/local-development/)

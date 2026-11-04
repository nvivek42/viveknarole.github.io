# Goal Clarity AI synthesis endpoint

The Goal Clarity page is hosted on GitHub Pages, which serves static files and cannot handle `POST /api/goal-clarity-synthesis`. That is why the browser currently receives HTTP 405. `workers/goal-clarity-synthesis.js` is a Cloudflare Worker backend for the existing page request. It keeps the NVIDIA API key server-side, checks the request origin, bounds the request size, does not log or persist submitted answers, and returns a synthesis or a safe error.

## Required deployment

This does **not** go live just by pushing this repository. Deploy the Worker in a Cloudflare account that manages the `viveknarole.com` DNS zone. The Wrangler route in `wrangler.toml` sends only `/api/goal-clarity-synthesis` to the Worker; GitHub Pages continues serving the static site. If DNS is not managed by Cloudflare, use another serverless host and configure the page endpoint to that host instead.

1. Install Wrangler and authenticate to the Cloudflare account that owns the `viveknarole.com` zone.
2. In NVIDIA's developer console, create an API key and choose a model available to that key/account.
3. Set the key as a Worker secret (never commit it or put it in browser JavaScript):

   ```sh
   npx wrangler secret put NVIDIA_API_KEY
   ```

4. Set `NIM_MODEL` in `wrangler.toml` to an inference model ID available to the NVIDIA account. Confirm the ID against that account's current NIM catalog.
5. Deploy from the repository root:

   ```sh
   npx wrangler deploy
   ```

6. Confirm the route responds to an `OPTIONS` preflight and a `POST` from `https://viveknarole.com`. The route must return JSON containing `{ "synthesis": "..." }` for a valid request.
7. Configure Cloudflare rate limiting and usage alerts for the route before announcing the AI feature publicly. The endpoint calls a metered/limited third-party AI service; do not treat origin checks as authentication or abuse prevention.

The worksheet asks for explicit consent before sending answers. Users should still avoid entering names or sensitive information. AI output is a reflection aid, not a recommendation or professional advice. Demo/worksheet mode and local draft saving continue to work if the AI service is not configured.

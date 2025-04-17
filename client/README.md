
This is a [Next.js](https://nextjs.org/) MCP client application, renamed from Next.js AI Lite, configured to talk to an MCP server (e.g., MCP Census Server).

## Getting Started

First, copy environment variables and run the development server:

yarn dev
```bash
cp .env.example .env.local
# Fill in OPENAI_API_KEY, NEXT_PUBLIC_MCP_SERVER_URL, NEXT_PUBLIC_SERVER_API_KEY in .env.local
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to access the MCP client UI and interact with your MCP server.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/basic-features/font-optimization) to automatically optimize and load Inter, a custom Google Font.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js/) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.

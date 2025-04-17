/** @type {import('next').NextConfig} */
const nextConfig = {
  // Proxy API requests to the MCP server to avoid CORS and mixed-content issues
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination:
          process.env.NEXT_PUBLIC_MCP_SERVER_URL +
          '/:path*',
      },
    ];
  },
};

export default nextConfig;

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: [],
    remotePatterns: [],
    unoptimized: true,
  },
  webpack: (config, { isServer }) => {
    // Handle large JSON files properly
    config.module.rules.push({
      test: /\.json$/,
      type: 'asset/resource',
      generator: {
        filename: 'static/[hash][ext]'
      }
    });

    // Increase the limit for large page data
    if (!isServer) {
      config.optimization.splitChunks.maxSize = 128 * 1024; // 128KB
    }

    return config;
  },
  // Increase the limit for page data size
  experimental: {
    largePageDataBytes: 128 * 1024 * 1024, // 128MB - increased to handle large GeoJSON data
  }
}

module.exports = nextConfig 